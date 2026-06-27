"""Register the Telegram webhook.

Run from the backend/ directory:  python set_webhook.py

By default it points Telegram at BACKEND_PUBLIC_URL (direct-to-FastAPI, e.g. via
a cloudflared/ngrok tunnel during dev). If you deploy the Cloudflare Worker,
pass the Worker URL instead:  python set_webhook.py https://your-worker.workers.dev
"""
import sys

import httpx

from app.config import settings


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else settings.backend_public_url
    if not base:
        raise SystemExit("Set BACKEND_PUBLIC_URL in .env or pass a URL argument.")

    # Direct-to-backend needs the /webhook/telegram path; a Worker root URL does not.
    url = base.rstrip("/")
    if "workers.dev" not in url and not url.endswith("/webhook/telegram"):
        url += "/webhook/telegram"

    r = httpx.post(
        f"https://api.telegram.org/bot{settings.telegram_bot_token}/setWebhook",
        json={
            "url": url,
            "secret_token": settings.telegram_secret_token,
            "allowed_updates": ["message"],
            "drop_pending_updates": True,
        },
        timeout=20,
    )
    print("setWebhook ->", r.json())

    info = httpx.get(
        f"https://api.telegram.org/bot{settings.telegram_bot_token}/getWebhookInfo",
        timeout=20,
    )
    print("getWebhookInfo ->", info.json())


if __name__ == "__main__":
    main()
