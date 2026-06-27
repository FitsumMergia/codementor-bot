"""FastAPI entry point.

The Cloudflare Worker (worker/) is the public front-door: it ACKs Telegram
instantly and forwards here. This app verifies the secret-token header, dedupes
update_id, and processes each update in a background task so the HTTP response
returns immediately (latency Risk #4).
"""
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from sqlalchemy import func, select

from .bot import handle_update
from .config import settings
from .db import engine, init_db, llm_usage, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="CodeMentor Chat AI — Phase 1", lifespan=lifespan)

# In-memory update_id dedup. The Worker also dedupes; a DB-backed window is a
# Phase 2 upgrade. Bounded so it can't grow without limit.
_seen_update_ids: set[int] = set()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/webhook/telegram")
async def telegram_webhook(
    request: Request,
    background: BackgroundTasks,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if x_telegram_bot_api_secret_token != settings.telegram_secret_token:
        raise HTTPException(status_code=403, detail="bad secret token")

    update = await request.json()
    uid = update.get("update_id")
    if uid is not None:
        if uid in _seen_update_ids:
            return {"ok": True}
        _seen_update_ids.add(uid)
        if len(_seen_update_ids) > 10_000:
            _seen_update_ids.clear()

    background.add_task(handle_update, update)
    return {"ok": True}


@app.get("/admin/metrics")
def metrics(token: str):
    """Quick read on the COGS ledger. Protected by ADMIN_TOKEN."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="forbidden")
    with engine.begin() as c:
        total_users = c.execute(select(func.count()).select_from(users)).scalar() or 0
        total_cost = c.execute(
            select(func.coalesce(func.sum(llm_usage.c.cost_usd), 0.0))
        ).scalar() or 0.0
        calls = c.execute(select(func.count()).select_from(llm_usage)).scalar() or 0
    return {
        "total_users": total_users,
        "llm_calls": calls,
        "total_llm_cost_usd": round(float(total_cost), 6),
        "avg_cost_per_user_usd": round(float(total_cost) / total_users, 6) if total_users else 0.0,
    }
