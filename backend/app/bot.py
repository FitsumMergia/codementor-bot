"""Bot brain — Phase 5: multi-track (Python 30 + JS 15), certificates, /language switch."""
from . import telegram as tg
from .ai_gateway import grade_submission, deep_review
from .certificate import generate_certificate
from .config import settings
from .intellisense import check_syntax, explain_keyword, get_hint, list_keywords
from .lessons import TRACKS, TRACK_INFO, get_track_lessons
from .repo import (
    apply_referral, check_and_increment_daily, count_passed, generate_voucher,
    get_admin_stats, get_bonus_reviews, get_leaderboard, get_or_create_referral_code,
    get_or_create_user, get_referral_count, get_session, get_streak,
    get_user_rank, get_user_tier, is_admin, list_users, list_vouchers,
    redeem_voucher, set_admin, set_session, update_streak, update_total_score,
    upsert_progress, use_bonus_review, FREE_DAILY_LIMIT, TIER_LIMITS,
    REFERRAL_REWARD_REVIEWS,
)

BOT_USERNAME = "ByteTutorAI_Bot"

WELCOME = (
    "<b>Welcome to CodeMentor!</b>\n\n"
    "I teach programming through chat. No experience needed.\n\n"
    "<b>Available tracks:</b>\n"
    "🐍 Python — {py_n} lessons (beginner → intermediate)\n"
    "🟨 JavaScript — {js_n} lessons (beginner)\n\n"
    "Starting with <b>{track_name}</b>...\n"
    "Switch anytime with /language"
)

HELP = (
    "<b>CodeMentor — commands</b>\n\n"
    "<b>Learning:</b>\n"
    "/start — begin from lesson 1\n"
    "/next — current lesson\n"
    "/hint — get a hint\n"
    "/explain — quick reference\n"
    "/language — switch track\n"
    "/progress — scores\n"
    "/streak — streak\n"
    "/certificate — get your certificate\n\n"
    "<b>Social:</b>\n"
    "/invite — share referral link\n"
    "/leaderboard — top learners\n\n"
    "<b>Account:</b>\n"
    "/mystatus — tier + limits\n"
    "/subscribe — upgrade\n"
    "/activate CODE — redeem\n"
    "/review — deep AI review (paid)\n\n"
    "/help — this message"
)

MILESTONES = {5: "5 lessons!", 10: "10 lessons!", 15: "15 done! 🏆", 20: "20! 🔥", 25: "25! Almost there!", 30: "ALL 30 COMPLETE! 🎉"}
STREAK_MSGS = {3: "3 days!", 7: "1 week!", 14: "2 weeks!", 30: "30 DAYS! 🔥"}


def handle_update(update: dict) -> None:
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return
    chat_id = msg.get("chat", {}).get("id")
    if chat_id is None:
        return
    frm = msg.get("from", {})
    text = (msg.get("text") or "").strip()
    name = frm.get("first_name") or "there"

    user_id = get_or_create_user("telegram", str(frm.get("id")), name, str(chat_id))
    state, idx, track = get_session(user_id)
    tier = get_user_tier(user_id)
    lessons = get_track_lessons(track)
    total = len(lessons)

    # Deep-link referral
    if text.startswith("/start") and " " in text:
        ref = text.split(maxsplit=1)[1].strip()
        if ref.upper().startswith("REF-"):
            ok, ref_msg, rid = apply_referral(user_id, ref)
            if ok:
                tg.send_message(chat_id, "🎉 " + ref_msg)
                if rid:
                    _notify_referrer(rid, name)
        _send_welcome(chat_id, user_id, track, lessons)
        return

    cmd = text.split()[0].lower() if text.startswith("/") else ""

    handlers = {
        "/start": lambda: _send_welcome(chat_id, user_id, track, lessons),
        "/help": lambda: tg.send_message(chat_id, HELP),
        "/next": lambda: _deliver_lesson(chat_id, user_id, idx, lessons, track) if idx < total else tg.send_message(chat_id, "🎉 Track complete! /certificate to get yours, or /language to try another."),
        "/hint": lambda: _handle_hint(chat_id, user_id, idx, state),
        "/explain": lambda: _handle_explain(chat_id, text),
        "/language": lambda: _handle_language(chat_id, user_id, track),
        "/progress": lambda: _show_progress(chat_id, user_id, idx, track, lessons),
        "/streak": lambda: _show_streak(chat_id, user_id),
        "/certificate": lambda: _handle_certificate(chat_id, user_id, name, track, lessons),
        "/invite": lambda: _handle_invite(chat_id, user_id),
        "/refer": lambda: _handle_refer(chat_id, user_id, text, name),
        "/leaderboard": lambda: _handle_leaderboard(chat_id, user_id),
        "/subscribe": lambda: _show_subscribe(chat_id, tier),
        "/activate": lambda: _handle_activate(chat_id, user_id, text),
        "/mystatus": lambda: _show_status(chat_id, user_id, tier),
        "/review": lambda: _handle_review(chat_id, user_id, idx, tier, lessons),
        "/admin": lambda: _handle_admin(chat_id, user_id),
        "/gencode": lambda: _handle_gencode(chat_id, user_id, text),
        "/stats": lambda: _handle_stats(chat_id, user_id),
        "/makeadmin": lambda: _handle_makeadmin(chat_id, user_id, text),
        "/codes": lambda: _handle_listcodes(chat_id, user_id),
        "/users": lambda: _handle_listusers(chat_id, user_id),
    }

    if cmd in handlers:
        handlers[cmd]()
        return

    if state == "AWAIT_SUBMISSION" and idx < total:
        _handle_submission(chat_id, user_id, idx, text, tier, track, lessons, name)
        return
    if state == "AWAIT_DEEP_REVIEW" and idx < total:
        _handle_deep_review_sub(chat_id, user_id, idx, text, lessons)
        return
    if state == "AWAIT_LANGUAGE":
        _process_language_choice(chat_id, user_id, text)
        return

    tg.send_message(chat_id, "Send /start to begin, or /help for commands.")


# ── Welcome + lesson delivery ────────────────────────────────────────

def _send_welcome(chat_id, user_id, track, lessons):
    info = TRACK_INFO
    tg.send_message(chat_id, WELCOME.format(
        py_n=info["python"]["lessons"], js_n=info["javascript"]["lessons"],
        track_name=info.get(track, info["python"])["name"],
    ))
    _deliver_lesson(chat_id, user_id, 0, lessons, track)


def _deliver_lesson(chat_id, user_id, idx, lessons, track):
    total = len(lessons)
    lesson = lessons[idx]
    emoji = TRACK_INFO.get(track, {}).get("emoji", "📖")
    header = "{e} <b>[{n}/{t}]</b> ".format(e=emoji, n=idx + 1, t=total)
    tg.send_message(chat_id, header + lesson["content"])
    set_session(user_id, "AWAIT_SUBMISSION", idx, track)


# ── Submission ───────────────────────────────────────────────────────

def _handle_submission(chat_id, user_id, idx, code, tier, track, lessons, name):
    if len(code) > 4000:
        tg.send_message(chat_id, "Keep code under 4000 chars.")
        return

    if track == "python":
        syntax_err = check_syntax(code)
        if syntax_err:
            tg.send_message(chat_id, syntax_err)
            tg.send_message(chat_id, "Fix it and resend. /hint for help.")
            return

    allowed, remaining = check_and_increment_daily(user_id)
    if not allowed:
        bonus = get_bonus_reviews(user_id)
        if bonus > 0 and use_bonus_review(user_id):
            remaining = bonus - 1
        else:
            limit = TIER_LIMITS.get(tier, FREE_DAILY_LIMIT)
            msg = "Used your <b>{l} reviews</b> today.".format(l=limit)
            if tier == "free":
                msg += "\n/invite for bonus reviews or /subscribe!"
            tg.send_message(chat_id, msg)
            return

    tg.typing(chat_id)
    tg.send_message(chat_id, "Reviewing...")

    result = grade_submission(user_id, lessons[idx], code)
    passed = bool(result.get("passed"))
    score = int(result.get("score") or 0)
    fb = tg.esc(result.get("feedback") or "")

    upsert_progress(user_id, idx, "passed" if passed else "failed", score)
    if score > 0:
        update_total_score(user_id, score)

    icon = "✅" if passed else "🔁"
    tg.send_message(chat_id, "{i} <b>{s}/100</b>\n\n{f}".format(i=icon, s=score, f=fb))

    total = len(lessons)

    if passed:
        streak = update_streak(user_id)
        nxt = idx + 1
        set_session(user_id, "IDLE", nxt, track)
        _hint_levels.pop(user_id, None)

        s_msg = STREAK_MSGS.get(streak)
        if s_msg:
            tg.send_message(chat_id, "🔥 " + s_msg)
        elif streak > 1:
            tg.send_message(chat_id, "🔥 {d}-day streak!".format(d=streak))

        done = count_passed(user_id)
        m_msg = MILESTONES.get(done)
        if m_msg:
            tg.send_message(chat_id, "🏆 " + m_msg)

        rank = get_user_rank(user_id)
        if rank and rank <= 10:
            tg.send_message(chat_id, "📊 #{r} on leaderboard!".format(r=rank))

        if nxt < total:
            tg.send_message(chat_id, "/next for lesson {n}.".format(n=nxt + 1))
        else:
            tg.send_message(chat_id, "🎉 <b>Track complete!</b> Send /certificate to get yours!")
    else:
        tg.send_message(chat_id, "Try again! /hint for help. 💪")

    if remaining <= 1 and remaining >= 0:
        bonus = get_bonus_reviews(user_id)
        extra = " +{b} bonus".format(b=bonus) if bonus else ""
        tg.send_message(chat_id, "📝 {r} review{s} left{x}.".format(r=remaining, s="" if remaining == 1 else "s", x=extra))


# ── Language switch ──────────────────────────────────────────────────

def _handle_language(chat_id, user_id, current_track):
    lines = ["<b>Choose your track:</b>", ""]
    for key, info in TRACK_INFO.items():
        current = " (current)" if key == current_track else ""
        lines.append("{e} <b>{n}</b> — {l} lessons{c}".format(
            e=info["emoji"], n=info["name"], l=info["lessons"], c=current
        ))
    lines.append("")
    lines.append("Send <code>python</code> or <code>javascript</code>")
    tg.send_message(chat_id, "\n".join(lines))
    set_session(user_id, "AWAIT_LANGUAGE", 0, current_track)


def _process_language_choice(chat_id, user_id, text):
    choice = text.strip().lower()
    if choice in ("python", "py", "🐍"):
        choice = "python"
    elif choice in ("javascript", "js", "🟨"):
        choice = "javascript"
    else:
        tg.send_message(chat_id, "Send <code>python</code> or <code>javascript</code>")
        return

    info = TRACK_INFO[choice]
    lessons = get_track_lessons(choice)
    set_session(user_id, "IDLE", 0, choice)
    tg.send_message(chat_id, "{e} Switched to <b>{n}</b> ({l} lessons)!\n\nSend /next to start.".format(
        e=info["emoji"], n=info["name"], l=info["lessons"]
    ))


# ── Certificate ──────────────────────────────────────────────────────

def _handle_certificate(chat_id, user_id, name, track, lessons):
    total = len(lessons)
    done = count_passed(user_id)
    if done < total:
        tg.send_message(chat_id, "Complete all {t} lessons first ({d}/{t} done). /next to continue.".format(t=total, d=done))
        return
    cert, code = generate_certificate(name, track, total, user_id)
    tg.send_message(chat_id, cert)
    tg.send_message(chat_id, "🎓 Share this with pride! Your verification code: <code>{c}</code>".format(c=code))


# ── Deep review ──────────────────────────────────────────────────────

def _handle_review(chat_id, user_id, idx, tier, lessons):
    if tier == "free":
        tg.send_message(chat_id, "Deep Review is paid. /subscribe to unlock!")
        return
    if idx == 0:
        tg.send_message(chat_id, "Complete a lesson first.")
        return
    from sqlalchemy import select
    from .db import engine, progress as p
    with engine.begin() as c:
        row = c.execute(select(p.c.lesson_index).where(p.c.user_id == user_id).order_by(p.c.updated_at.desc()).limit(1)).first()
    if not row:
        tg.send_message(chat_id, "Submit code first.")
        return
    li = row[0]
    tg.send_message(chat_id, "Send code for <b>L{n}: {t}</b> for deep review.".format(n=li+1, t=lessons[li]["topic"]))
    set_session(user_id, "AWAIT_DEEP_REVIEW", li)


def _handle_deep_review_sub(chat_id, user_id, idx, code, lessons):
    if len(code) > 4000:
        tg.send_message(chat_id, "Keep under 4000 chars.")
        return
    tg.typing(chat_id)
    tg.send_message(chat_id, "Running deep review...")
    result = deep_review(user_id, lessons[idx], code)
    score = int(result.get("score") or 0)
    icon = "✅" if result.get("passed") else "🔁"
    fb = tg.esc(result.get("feedback") or "")
    tg.send_message(chat_id, "🔍 <b>Deep Review — {s}/100</b> {i}\n\n{f}".format(s=score, i=icon, f=fb))
    set_session(user_id, "IDLE", idx)


# ── Referrals ────────────────────────────────────────────────────────

def _handle_invite(chat_id, user_id):
    code = get_or_create_referral_code(user_id)
    count = get_referral_count(user_id)
    bonus = get_bonus_reviews(user_id)
    link = "https://t.me/{bot}?start={code}".format(bot=BOT_USERNAME, code=code)
    tg.send_message(chat_id, (
        "<b>Invite friends!</b>\n\n"
        "Link: {link}\nCode: <code>{code}</code>\n\n"
        "Friends joined: <b>{c}</b>\nBonus reviews: <b>{b}</b>\n\n"
        "Each friend = <b>{r} bonus reviews</b>!"
    ).format(link=link, code=code, c=count, b=bonus, r=REFERRAL_REWARD_REVIEWS))

def _handle_refer(chat_id, user_id, text, name):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        tg.send_message(chat_id, "Usage: /refer REF-XXXXXX")
        return
    ok, msg, rid = apply_referral(user_id, parts[1].strip())
    tg.send_message(chat_id, ("🎉 " if ok else "❌ ") + msg)
    if ok and rid:
        _notify_referrer(rid, name)

def _notify_referrer(referrer_id, new_name):
    from sqlalchemy import select
    from .db import engine, users as u
    with engine.begin() as c:
        row = c.execute(select(u.c.chat_id).where(u.c.id == referrer_id)).first()
    if row and row[0]:
        tg.send_message(int(row[0]), "🎉 <b>{n}</b> joined via your invite! +{r} bonus reviews.".format(n=tg.esc(new_name), r=REFERRAL_REWARD_REVIEWS))


# ── Leaderboard ──────────────────────────────────────────────────────

def _handle_leaderboard(chat_id, user_id):
    board = get_leaderboard(10)
    if not board:
        tg.send_message(chat_id, "No scores yet! /start")
        return
    medals = ["🥇", "🥈", "🥉"]
    lines = ["<b>🏆 Leaderboard</b>", ""]
    for i, e in enumerate(board):
        p = medals[i] if i < 3 else " {n}.".format(n=i+1)
        stk = " 🔥{s}".format(s=e["streak"]) if e["streak"] > 0 else ""
        lines.append("{p} <b>{name}</b> — {score}pts{s}".format(p=p, name=tg.esc(e["name"]), score=e["score"], s=stk))
    rank = get_user_rank(user_id)
    if rank:
        lines.extend(["", "Your rank: <b>#{r}</b>".format(r=rank)])
    tg.send_message(chat_id, "\n".join(lines))


# ── Progress ─────────────────────────────────────────────────────────

def _show_progress(chat_id, user_id, current_idx, track, lessons):
    from sqlalchemy import select
    from .db import engine, progress as pt
    done = count_passed(user_id)
    streak = get_streak(user_id)
    tier = get_user_tier(user_id)
    rank = get_user_rank(user_id)
    total = len(lessons)
    info = TRACK_INFO.get(track, TRACK_INFO["python"])

    lines = [
        "<b>{e} {tn} Progress</b>".format(e=info["emoji"], tn=info["name"]),
        "Passed: <b>{d}/{t}</b> | Streak: <b>{s}</b> 🔥{r}".format(
            d=done, t=total, s="{d}d".format(d=streak) if streak else "—",
            r=" | #{r}".format(r=rank) if rank else ""
        ), "",
    ]
    with engine.begin() as c:
        rows = c.execute(select(pt.c.lesson_index, pt.c.status, pt.c.score).where(pt.c.user_id == user_id).order_by(pt.c.lesson_index)).fetchall()
        pmap = {r[0]: (r[1], r[2]) for r in rows}
    for i, lesson in enumerate(lessons):
        if i in pmap:
            st, sc = pmap[i]
            ic = "✅" if st == "passed" else "❌"
            lines.append("{ic} L{n}: {t} ({s})".format(ic=ic, n=i+1, t=lesson["topic"], s=sc))
        elif i == current_idx:
            lines.append("👉 L{n}: {t}".format(n=i+1, t=lesson["topic"]))
        elif i < current_idx + 3:
            lines.append("⬜ L{n}: {t}".format(n=i+1, t=lesson["topic"]))
    if total > current_idx + 3:
        remaining = total - min(current_idx + 3, total)
        if remaining > 0:
            lines.append("... +{r} more".format(r=remaining))
    tg.send_message(chat_id, "\n".join(lines))


def _show_streak(chat_id, user_id):
    s = get_streak(user_id)
    if s == 0:
        tg.send_message(chat_id, "No streak yet. /next to start! 🔥")
    else:
        bar = "🟩" * min(s, 14) + ("..." if s > 14 else "")
        tg.send_message(chat_id, "🔥 <b>{d}-day streak!</b>\n\n{bar}".format(d=s, bar=bar))


# ── Subscription ─────────────────────────────────────────────────────

def _show_subscribe(chat_id, tier):
    if tier != "free":
        tg.send_message(chat_id, "You're on <b>{t}</b>! /mystatus".format(t=tier.capitalize()))
        return
    tg.send_message(chat_id, (
        "<b>Upgrade CodeMentor</b>\n\n"
        "<b>Free:</b> {fl} reviews/day\n"
        "<b>Standard (ETB {sm}/mo):</b> {sl} reviews/day\n"
        "<b>Pro (ETB {pm}/mo):</b> Unlimited + Deep Review\n\n"
        "Send payment via Telebirr, get a code, /activate it.\n"
        "Or /invite friends for bonus reviews!"
    ).format(fl=FREE_DAILY_LIMIT, sl=settings.standard_daily_limit, sm=settings.price_standard_monthly, pm=settings.price_pro_monthly))

def _handle_activate(chat_id, user_id, text):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        tg.send_message(chat_id, "Usage: /activate CM-XXXXXXXX")
        return
    ok, msg = redeem_voucher(user_id, parts[1].strip())
    tg.send_message(chat_id, ("✅ " if ok else "❌ ") + msg)

def _show_status(chat_id, user_id, tier):
    from datetime import date as d
    from sqlalchemy import select
    from .db import engine, users as u
    with engine.begin() as c:
        row = c.execute(select(u.c.subscription_expires_at, u.c.daily_submissions, u.c.daily_submissions_date, u.c.bonus_reviews).where(u.c.id == user_id)).first()
    limit = TIER_LIMITS.get(tier, FREE_DAILY_LIMIT)
    used = row[1] or 0
    if row[2] != d.today():
        used = 0
    bonus = row[3] or 0
    refs = get_referral_count(user_id)
    code = get_or_create_referral_code(user_id)
    _, _, track = get_session(user_id)
    lines = [
        "<b>Account</b>",
        "Tier: <b>{t}</b>".format(t=tier.capitalize()),
        "Track: <b>{tn}</b>".format(tn=TRACK_INFO.get(track, {}).get("name", track)),
    ]
    if tier != "free" and row[0]:
        lines.append("Expires: {d}".format(d=row[0].isoformat()))
    lines.append("Reviews: {u}/{l}{b}".format(u=used, l=limit, b=" +{b} bonus".format(b=bonus) if bonus else ""))
    lines.append("Referrals: {r} | Code: <code>{c}</code>".format(r=refs, c=code))
    tg.send_message(chat_id, "\n".join(lines))


# ── Intellisense ─────────────────────────────────────────────────────

_hint_levels: dict[int, int] = {}

def _handle_hint(chat_id, user_id, idx, state):
    if state != "AWAIT_SUBMISSION":
        tg.send_message(chat_id, "/next first, then /hint when stuck.")
        return
    level = _hint_levels.get(user_id, 0)
    hint_text, next_level = get_hint(idx, level)
    _hint_levels[user_id] = next_level
    r = 2 - level
    if r > 0:
        hint_text += "\n\n/hint again ({r} left).".format(r=r)
    tg.send_message(chat_id, hint_text)

def _handle_explain(chat_id, text):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        tg.send_message(chat_id, "<b>Quick Reference</b>\n\n<code>/explain keyword</code>\n\nTopics: {kw}".format(kw=list_keywords()))
        return
    exp = explain_keyword(parts[1].strip())
    if exp:
        tg.send_message(chat_id, exp)
    else:
        tg.send_message(chat_id, "No ref for <code>{k}</code>. Try: {kw}".format(k=tg.esc(parts[1]), kw=list_keywords()))


# ── Admin ────────────────────────────────────────────────────────────

def _handle_admin(chat_id, user_id):
    if not is_admin(user_id): return tg.send_message(chat_id, "Admin required.")
    tg.send_message(chat_id, "<b>Admin</b>\n/stats /gencode /codes /users /makeadmin")

def _handle_gencode(chat_id, user_id, text):
    if not is_admin(user_id): return
    parts = text.split()
    if len(parts) < 3: return tg.send_message(chat_id, "/gencode standard 30")
    tier = parts[1].lower()
    if tier not in ("standard","pro"): return tg.send_message(chat_id, "standard or pro")
    try: days = int(parts[2])
    except ValueError: return tg.send_message(chat_id, "Days = number")
    code = generate_voucher(tier, days)
    tg.send_message(chat_id, "✅ <b>{t}</b> ({d}d): <code>{c}</code>\nUser: /activate {c}".format(t=tier.capitalize(), d=days, c=code))

def _handle_stats(chat_id, user_id):
    if not is_admin(user_id): return
    s = get_admin_stats()
    tg.send_message(chat_id, "<b>Dashboard</b>\nUsers: {tu} (paid:{pu})\nConversion: {cv}%\nRevenue: ETB {rev}\nCost: ${cost}\nCalls: {calls}".format(**s))

def _handle_listcodes(chat_id, user_id):
    if not is_admin(user_id): return
    codes = list_vouchers(True)
    if not codes: return tg.send_message(chat_id, "None. /gencode standard 30")
    lines = ["<b>Vouchers</b>",""]
    for v in codes: lines.append("<code>{code}</code> {tier} ({days}d)".format(**v))
    tg.send_message(chat_id, "\n".join(lines))

def _handle_listusers(chat_id, user_id):
    if not is_admin(user_id): return
    ul = list_users(20)
    if not ul: return tg.send_message(chat_id, "No users.")
    lines = ["<b>Users</b>",""]
    for u in ul: lines.append("#{id} {name} | {tier} | {score}pts | {last_active}".format(**u))
    tg.send_message(chat_id, "\n".join(lines))

def _handle_makeadmin(chat_id, user_id, text):
    if not is_admin(user_id):
        from sqlalchemy import select
        from .db import engine, users as u
        with engine.begin() as c:
            if not c.execute(select(u.c.id).where(u.c.is_admin == 1)).first():
                set_admin(user_id)
                return tg.send_message(chat_id, "✅ You're admin! /admin")
        return tg.send_message(chat_id, "Admin required.")
    parts = text.split()
    if len(parts) < 2: return tg.send_message(chat_id, "/makeadmin USER_ID")
    try: tid = int(parts[1])
    except ValueError: return tg.send_message(chat_id, "Number required.")
    set_admin(tid)
    tg.send_message(chat_id, "✅ User {u} is admin.".format(u=tid))
