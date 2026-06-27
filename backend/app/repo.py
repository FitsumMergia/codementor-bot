"""Data-access helpers. Phase 4: referrals, leaderboard, bonus reviews."""
import secrets
import string
from datetime import date, timedelta, datetime

from sqlalchemy import select, insert, update, func

from .config import settings
from .db import engine, users, sessions, progress, vouchers, payments


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def get_or_create_user(platform: str, platform_user_id: str, name: str, chat_id: str = "") -> int:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.id).where(
                users.c.platform == platform,
                users.c.platform_user_id == platform_user_id,
            )
        ).first()
        if row:
            vals = {"last_active_at": func.now()}
            if chat_id:
                vals["chat_id"] = chat_id
            c.execute(update(users).where(users.c.id == row[0]).values(**vals))
            return row[0]
        res = c.execute(
            insert(users).values(
                platform=platform, platform_user_id=platform_user_id,
                name=name, chat_id=chat_id,
            )
        )
        return int(res.inserted_primary_key[0])


def get_user_tier(user_id: int) -> str:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.subscription_status, users.c.subscription_expires_at)
            .where(users.c.id == user_id)
        ).first()
        if not row:
            return "free"
        status, expires = row[0] or "free", row[1]
        if status in ("standard", "pro"):
            if expires and expires < date.today():
                c.execute(
                    update(users).where(users.c.id == user_id)
                    .values(subscription_status="free", subscription_expires_at=None)
                )
                return "free"
            return status
        return "free"


def is_admin(user_id: int) -> bool:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.is_admin).where(users.c.id == user_id)
        ).first()
        return bool(row and row[0])


def set_admin(user_id: int) -> None:
    with engine.begin() as c:
        c.execute(update(users).where(users.c.id == user_id).values(is_admin=1))


# ---------------------------------------------------------------------------
# Streaks
# ---------------------------------------------------------------------------

def update_streak(user_id: int) -> int:
    today = date.today()
    with engine.begin() as c:
        row = c.execute(
            select(users.c.streak_days, users.c.streak_last_date)
            .where(users.c.id == user_id)
        ).first()
        if not row:
            return 0
        streak, last_date = row[0] or 0, row[1]
        if last_date == today:
            return streak
        if last_date == today - timedelta(days=1):
            streak += 1
        else:
            streak = 1
        c.execute(
            update(users).where(users.c.id == user_id)
            .values(streak_days=streak, streak_last_date=today)
        )
        return streak


def get_streak(user_id: int) -> int:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.streak_days, users.c.streak_last_date)
            .where(users.c.id == user_id)
        ).first()
        if not row:
            return 0
        streak, last_date = row[0] or 0, row[1]
        if last_date is None or last_date < date.today() - timedelta(days=1):
            return 0
        return streak


# ---------------------------------------------------------------------------
# Rate limiting (tier-aware)
# ---------------------------------------------------------------------------

TIER_LIMITS = {
    "free": settings.free_daily_limit,
    "standard": settings.standard_daily_limit,
    "pro": settings.pro_daily_limit,
}
FREE_DAILY_LIMIT = settings.free_daily_limit


def check_and_increment_daily(user_id: int) -> tuple[bool, int]:
    """Returns (allowed, remaining)."""
    today = date.today()
    with engine.begin() as c:
        row = c.execute(
            select(
                users.c.daily_submissions,
                users.c.daily_submissions_date,
                users.c.subscription_status,
            ).where(users.c.id == user_id)
        ).first()
        if not row:
            return False, 0

        count, count_date, sub = row[0] or 0, row[1], row[2] or "free"
        limit = TIER_LIMITS.get(sub, FREE_DAILY_LIMIT)

        if count_date != today:
            count = 0

        if count >= limit:
            return False, 0

        c.execute(
            update(users).where(users.c.id == user_id)
            .values(daily_submissions=count + 1, daily_submissions_date=today)
        )
        return True, limit - count - 1


# ---------------------------------------------------------------------------
# Vouchers
# ---------------------------------------------------------------------------

def generate_voucher(tier: str, days: int) -> str:
    code = "CM-" + "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    with engine.begin() as c:
        c.execute(insert(vouchers).values(code=code, tier=tier, days=days))
    return code


def redeem_voucher(user_id: int, code: str) -> tuple[bool, str]:
    """Returns (success, message)."""
    code = code.strip().upper()
    with engine.begin() as c:
        row = c.execute(
            select(vouchers.c.id, vouchers.c.tier, vouchers.c.days, vouchers.c.redeemed_by)
            .where(vouchers.c.code == code)
        ).first()

        if not row:
            return False, "Invalid code. Check the code and try again."

        vid, tier, days, redeemed_by = row
        if redeemed_by is not None:
            return False, "This code has already been used."

        expires = date.today() + timedelta(days=days)

        c.execute(
            update(vouchers).where(vouchers.c.id == vid)
            .values(redeemed_by=user_id, redeemed_at=func.now())
        )
        c.execute(
            update(users).where(users.c.id == user_id)
            .values(subscription_status=tier, subscription_expires_at=expires)
        )
        c.execute(insert(payments).values(
            user_id=user_id,
            amount_etb=settings.price_standard_monthly if tier == "standard" else settings.price_pro_monthly,
            tier=tier, days=days, voucher_code=code, method="voucher",
        ))
        return True, "Activated <b>{tier}</b> for {days} days (expires {exp}).".format(
            tier=tier.capitalize(), days=days, exp=expires.isoformat()
        )


def list_vouchers(unused_only: bool = True) -> list[dict]:
    with engine.begin() as c:
        q = select(vouchers.c.code, vouchers.c.tier, vouchers.c.days, vouchers.c.redeemed_by)
        if unused_only:
            q = q.where(vouchers.c.redeemed_by.is_(None))
        rows = c.execute(q.order_by(vouchers.c.id.desc()).limit(20)).fetchall()
        return [{"code": r[0], "tier": r[1], "days": r[2], "used": r[3] is not None} for r in rows]


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

def get_session(user_id: int) -> tuple[str, int, str]:
    """Returns (state, lesson_index, track)."""
    with engine.begin() as c:
        row = c.execute(
            select(sessions.c.state, sessions.c.current_lesson_index, sessions.c.track)
            .where(sessions.c.user_id == user_id)
        ).first()
        if row:
            return row[0], row[1], row[2] or "python"
        c.execute(insert(sessions).values(user_id=user_id, state="IDLE", current_lesson_index=0, track="python"))
        return "IDLE", 0, "python"


def set_session(user_id: int, state: str, index: int, track: str | None = None) -> None:
    with engine.begin() as c:
        exists = c.execute(
            select(sessions.c.user_id).where(sessions.c.user_id == user_id)
        ).first()
        vals = {"state": state, "current_lesson_index": index, "updated_at": func.now()}
        if track is not None:
            vals["track"] = track
        if exists:
            c.execute(update(sessions).where(sessions.c.user_id == user_id).values(**vals))
        else:
            if track is None:
                vals["track"] = "python"
            c.execute(insert(sessions).values(user_id=user_id, **vals))


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------

def upsert_progress(user_id: int, lesson_index: int, status: str, score: int) -> None:
    with engine.begin() as c:
        row = c.execute(
            select(progress.c.id, progress.c.attempts).where(
                progress.c.user_id == user_id,
                progress.c.lesson_index == lesson_index,
            )
        ).first()
        if row:
            c.execute(
                update(progress).where(progress.c.id == row[0])
                .values(status=status, score=score, attempts=row[1] + 1, updated_at=func.now())
            )
        else:
            c.execute(insert(progress).values(
                user_id=user_id, lesson_index=lesson_index,
                status=status, score=score, attempts=1,
            ))


def count_passed(user_id: int) -> int:
    with engine.begin() as c:
        return c.execute(
            select(func.count()).select_from(progress).where(
                progress.c.user_id == user_id,
                progress.c.status == "passed",
            )
        ).scalar() or 0


# ---------------------------------------------------------------------------
# Admin stats
# ---------------------------------------------------------------------------

def get_admin_stats() -> dict:
    with engine.begin() as c:
        total_users = c.execute(select(func.count()).select_from(users)).scalar() or 0
        paid = c.execute(
            select(func.count()).select_from(users)
            .where(users.c.subscription_status.in_(["standard", "pro"]))
        ).scalar() or 0
        total_cost = c.execute(
            select(func.coalesce(func.sum(llm_usage.c.cost_usd), 0.0))
        ).scalar() or 0.0
        total_revenue = c.execute(
            select(func.coalesce(func.sum(payments.c.amount_etb), 0.0))
        ).scalar() or 0.0
        calls = c.execute(select(func.count()).select_from(llm_usage)).scalar() or 0
        return {
            "total_users": total_users,
            "paid_users": paid,
            "free_users": total_users - paid,
            "conversion_pct": round(paid / total_users * 100, 1) if total_users else 0,
            "total_revenue_etb": round(float(total_revenue)),
            "total_llm_cost_usd": round(float(total_cost), 4),
            "llm_calls": calls,
        }


# ---------------------------------------------------------------------------
# Daily push
# ---------------------------------------------------------------------------

def get_all_chat_ids() -> list[tuple[int, str, str, int]]:
    with engine.begin() as c:
        rows = c.execute(
            select(
                users.c.id, users.c.chat_id, users.c.name,
                sessions.c.current_lesson_index,
            )
            .select_from(users.join(sessions, users.c.id == sessions.c.user_id, isouter=True))
            .where(users.c.chat_id.isnot(None), users.c.chat_id != "")
        ).fetchall()
        return [(r[0], r[1], r[2] or "there", r[3] or 0) for r in rows]


# ---------------------------------------------------------------------------
# Referrals
# ---------------------------------------------------------------------------

REFERRAL_REWARD_REVIEWS = 3
REFERRAL_MILESTONE = 3


def get_or_create_referral_code(user_id: int) -> str:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.referral_code).where(users.c.id == user_id)
        ).first()
        if row and row[0]:
            return row[0]
        code = "REF-" + "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        c.execute(update(users).where(users.c.id == user_id).values(referral_code=code))
        return code


def apply_referral(new_user_id: int, referral_code: str) -> tuple[bool, str, int | None]:
    """Apply a referral when a new user starts. Returns (success, message, referrer_user_id)."""
    referral_code = referral_code.strip().upper()
    with engine.begin() as c:
        already = c.execute(
            select(users.c.referred_by).where(users.c.id == new_user_id)
        ).first()
        if already and already[0]:
            return False, "You've already used a referral code.", None

        referrer = c.execute(
            select(users.c.id, users.c.name).where(users.c.referral_code == referral_code)
        ).first()
        if not referrer:
            return False, "Invalid referral code.", None

        if referrer[0] == new_user_id:
            return False, "You can't refer yourself.", None

        c.execute(
            update(users).where(users.c.id == new_user_id)
            .values(referred_by=referrer[0])
        )
        c.execute(
            update(users).where(users.c.id == referrer[0])
            .values(bonus_reviews=users.c.bonus_reviews + REFERRAL_REWARD_REVIEWS)
        )
        return True, "Referred by {n}! They earned {r} bonus reviews.".format(
            n=referrer[1], r=REFERRAL_REWARD_REVIEWS
        ), referrer[0]


def get_referral_count(user_id: int) -> int:
    with engine.begin() as c:
        return c.execute(
            select(func.count()).select_from(users)
            .where(users.c.referred_by == user_id)
        ).scalar() or 0


def get_bonus_reviews(user_id: int) -> int:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.bonus_reviews).where(users.c.id == user_id)
        ).first()
        return row[0] if row else 0


def use_bonus_review(user_id: int) -> bool:
    with engine.begin() as c:
        row = c.execute(
            select(users.c.bonus_reviews).where(users.c.id == user_id)
        ).first()
        if not row or row[0] <= 0:
            return False
        c.execute(
            update(users).where(users.c.id == user_id)
            .values(bonus_reviews=users.c.bonus_reviews - 1)
        )
        return True


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------

def update_total_score(user_id: int, score: int) -> None:
    with engine.begin() as c:
        c.execute(
            update(users).where(users.c.id == user_id)
            .values(total_score=users.c.total_score + score)
        )


def get_leaderboard(limit: int = 10) -> list[dict]:
    with engine.begin() as c:
        rows = c.execute(
            select(users.c.name, users.c.total_score, users.c.streak_days)
            .where(users.c.total_score > 0)
            .order_by(users.c.total_score.desc())
            .limit(limit)
        ).fetchall()
        return [{"name": r[0] or "Anonymous", "score": r[1], "streak": r[2] or 0} for r in rows]


def get_user_rank(user_id: int) -> int | None:
    with engine.begin() as c:
        user_score = c.execute(
            select(users.c.total_score).where(users.c.id == user_id)
        ).scalar() or 0
        if user_score == 0:
            return None
        rank = c.execute(
            select(func.count()).select_from(users)
            .where(users.c.total_score > user_score)
        ).scalar() or 0
        return rank + 1


# ---------------------------------------------------------------------------
# Admin: user management
# ---------------------------------------------------------------------------

def list_users(limit: int = 20) -> list[dict]:
    with engine.begin() as c:
        rows = c.execute(
            select(
                users.c.id, users.c.name, users.c.subscription_status,
                users.c.total_score, users.c.streak_days, users.c.last_active_at,
            ).order_by(users.c.last_active_at.desc()).limit(limit)
        ).fetchall()
        return [{
            "id": r[0], "name": r[1] or "?", "tier": r[2] or "free",
            "score": r[3] or 0, "streak": r[4] or 0,
            "last_active": str(r[5])[:10] if r[5] else "?",
        } for r in rows]


# Need this import at module scope for get_admin_stats
from .db import llm_usage, payments  # noqa: E402
