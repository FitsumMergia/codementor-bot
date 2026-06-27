"""Database schema. SQLAlchemy Core — portable across SQLite and MySQL.

Phase 4 additions: referred_by + referral_code on users, referrals table.
"""
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, DateTime, Date, UniqueConstraint, func,
)

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("platform", String(20), nullable=False),
    Column("platform_user_id", String(64), nullable=False),
    Column("chat_id", String(64)),
    Column("name", String(120)),
    Column("subscription_status", String(20), default="free"),
    Column("subscription_expires_at", Date, nullable=True),
    Column("streak_days", Integer, default=0),
    Column("streak_last_date", Date, nullable=True),
    Column("daily_submissions", Integer, default=0),
    Column("daily_submissions_date", Date, nullable=True),
    Column("is_admin", Integer, default=0),
    Column("referral_code", String(20), nullable=True, unique=True),
    Column("referred_by", Integer, nullable=True),
    Column("bonus_reviews", Integer, default=0),
    Column("total_score", Integer, default=0),
    Column("created_at", DateTime, server_default=func.now()),
    Column("last_active_at", DateTime, server_default=func.now()),
    UniqueConstraint("platform", "platform_user_id", name="uq_platform_user"),
)

sessions = Table(
    "sessions", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("state", String(40), default="IDLE"),
    Column("current_lesson_index", Integer, default=0),
    Column("track", String(20), default="python"),
    Column("updated_at", DateTime, server_default=func.now()),
)

progress = Table(
    "progress", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("lesson_index", Integer, nullable=False),
    Column("status", String(20), default="in_progress"),
    Column("score", Integer, default=0),
    Column("attempts", Integer, default=0),
    Column("updated_at", DateTime, server_default=func.now()),
    UniqueConstraint("user_id", "lesson_index", name="uq_user_lesson"),
)

llm_usage = Table(
    "llm_usage", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("model", String(40)),
    Column("feature", String(40)),
    Column("input_tokens", Integer, default=0),
    Column("cache_read_tokens", Integer, default=0),
    Column("cache_write_tokens", Integer, default=0),
    Column("output_tokens", Integer, default=0),
    Column("cost_usd", Float, default=0.0),
    Column("created_at", DateTime, server_default=func.now()),
)

vouchers = Table(
    "vouchers", metadata,
    Column("id", Integer, primary_key=True),
    Column("code", String(20), nullable=False, unique=True),
    Column("tier", String(20), nullable=False),
    Column("days", Integer, nullable=False),
    Column("redeemed_by", Integer, nullable=True),
    Column("redeemed_at", DateTime, nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
)

payments = Table(
    "payments", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("amount_etb", Float, nullable=False),
    Column("tier", String(20), nullable=False),
    Column("days", Integer, nullable=False),
    Column("voucher_code", String(20)),
    Column("method", String(30), default="voucher"),
    Column("created_at", DateTime, server_default=func.now()),
)


def init_db() -> None:
    metadata.create_all(engine)
