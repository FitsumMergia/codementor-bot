# CodeMentor Chat AI — Phase 1 (Walking Skeleton)

A Telegram bot that teaches Python by setting short exercises, reading the code
you send back, and grading it with Claude. This is **Phase 1** of the roadmap:
the goal is to validate *"do people use it?"* and *"is the per-user LLM cost what
we modeled?"* — not to be feature-complete.

## What's here

```
backend/
  app/
    main.py        FastAPI: webhook, secret-token check, update_id dedup, /admin/metrics
    bot.py         State machine + lesson flow
    ai_gateway.py  THE cost chokepoint: Haiku 4.5, prompt caching, usage ledger
    lessons.py     5 hardcoded Python micro-lessons
    repo.py        DB access helpers (portable SQLite/MySQL)
    db.py          Schema: users, sessions, progress, llm_usage
    telegram.py    Telegram Bot API client (HTML)
    config.py      Settings from .env
  set_webhook.py   Register the Telegram webhook
  requirements.txt
  .env.example
worker/
  worker.js        Cloudflare Worker front-door (instant 200 ACK)
  wrangler.toml
```

Architecture: `Telegram → Cloudflare Worker (instant 200) → FastAPI (background) → Claude + MySQL`.
The Worker is what lets us honour Telegram's fast-ACK requirement while an LLM
call takes 2–4s.

## Prerequisites

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An Anthropic API key
- (Prod) a MySQL database; (dev) nothing — defaults to local SQLite

## Run it locally

```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate    # Windows; use bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env          # then fill in TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY,
                              # and a random TELEGRAM_SECRET_TOKEN
uvicorn app.main:app --reload --port 8000
```

The DB tables auto-create on startup. Check it's alive: `curl localhost:8000/health`.

## Expose the backend + register the webhook

Telegram needs a public HTTPS URL. For dev, tunnel port 8000:

```bash
cloudflared tunnel --url http://localhost:8000      # or: ngrok http 8000
```

Put the tunnel URL in `.env` as `BACKEND_PUBLIC_URL`, then:

```bash
python set_webhook.py
```

Message your bot `/start` and walk the 5 lessons.

## Production front-door (Cloudflare Worker)

```bash
cd worker
npx wrangler secret put TELEGRAM_SECRET_TOKEN   # same value as backend .env
npx wrangler secret put BACKEND_URL             # your deployed FastAPI URL
npx wrangler deploy
# point Telegram at the Worker instead of the backend:
cd ../backend && python set_webhook.py https://codementor-relay.<subdomain>.workers.dev
```

## Watch the unit economics

The whole business case rests on per-user LLM cost. Every Claude call is logged
to the `llm_usage` table with a computed USD cost. Read the rollup:

```bash
curl "localhost:8000/admin/metrics?token=YOUR_ADMIN_TOKEN"
# -> { total_users, llm_calls, total_llm_cost_usd, avg_cost_per_user_usd }
```

Compare `avg_cost_per_user_usd` against the modeled ~$0.35/free-user/month
before locking pricing.

## Phase-1 quality gate (from the roadmap)

- [ ] 50 real users onboarded, zero webhook-timeout incidents
- [ ] One full lesson → exercise → feedback loop works on a real phone
- [ ] `llm_usage` populated; measured cost/active-user within ~2× of model
- [ ] ≥40% of activated users complete ≥3 lessons

## Known Phase-1 limitations (deliberate)

- **No user-code execution** — grading is static LLM evaluation (safer, cheaper).
  Sandbox is a Phase-5 decision gated on data.
- **Prompt caching may not engage yet** — Haiku's minimum cacheable prefix is
  4096 tokens; the system prompt + one rubric can sit just under it. The
  `cache_control` marker is correctly placed and engages as the prompt bank grows.
  Verify with `cache_read_tokens > 0` in `llm_usage`.
- **In-memory `update_id` dedup** — fine at this scale; DB-backed window is Phase 2.
- **Lessons hardcoded** — they move to the Google Sheets CMS in Phase 2.
- **No payments** — that's Phase 3 (and needs a local rail like Telebirr, not cards).
