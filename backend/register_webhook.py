"""Register the Telegram webhook with an ngrok tunnel URL.

Usage:
  python register_webhook.py https://xxxx-xx-xx.ngrok-free.app

Grabs the URL from ngrok's local API if no argument is given.
"""
import sys
import httpx
from app.config import settings


def get_ngrok_url() -> str:
    try:
        r = httpx.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
        tunnels = r.json().get("tunnels", [])
        for t in tunnels:
            if t.get("proto") == "https":
                return t["public_url"]
        if tunnels:
            return tunnels[0]["public_url"]
    except Exception:
        pass
    return ""


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else get_ngrok_url()
    if not url:
        raise SystemExit(
            "No URL provided and could not auto-detect ngrok tunnel.\n"
            "Start ngrok first (tunnel.bat), then re-run this script."
        )
    webhook_url = url.rstrip("/") + "/webhook/telegram"
    print(f"Registering webhook: {webhook_url}")

    r = httpx.post(
        f"https://api.telegram.org/bot{settings.telegram_bot_token}/setWebhook",
        json={
            "url": webhook_url,
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
    result = info.json().get("result", {})
    print(f"Webhook URL: {result.get('url')}")
    print(f"Pending updates: {result.get('pending_update_count', 0)}")
    if result.get("last_error_message"):
        print(f"Last error: {result['last_error_message']}")
    else:
        print("Status: OK - no errors")


if __name__ == "__main__":
    main()
