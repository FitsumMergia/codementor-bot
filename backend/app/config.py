"""Application configuration, loaded from environment / .env."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Telegram
    telegram_bot_token: str = ""
    telegram_secret_token: str = "change-me"

    # AI providers — picks first with a key: Gemini → Claude → local
    gemini_api_key: str = ""
    anthropic_api_key: str = ""

    # Storage
    database_url: str = "sqlite:///./codementor.db"

    # Admin — your Telegram user ID (set after first /start)
    admin_token: str = "change-me-admin"
    admin_chat_id: str = ""

    # Model routing
    grader_model: str = "claude-haiku-4-5"
    review_model: str = "claude-sonnet-4-6"

    # Public URL
    backend_public_url: str = ""

    # SSL (corporate proxy)
    ssl_verify: bool = False

    # Tier limits (daily graded submissions)
    free_daily_limit: int = 3
    standard_daily_limit: int = 15
    pro_daily_limit: int = 999

    # Pricing display (ETB)
    price_standard_monthly: int = 199
    price_pro_monthly: int = 399
    price_standard_annual: int = 1990
    price_pro_annual: int = 3990


settings = Settings()
