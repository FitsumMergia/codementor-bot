"""Minimal Telegram Bot API client. All messages use parse_mode=HTML;
caller-supplied dynamic text must be passed through esc() first.
"""
import html

import httpx

from .config import settings

_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}"
_HTTP = httpx.Client(verify=settings.ssl_verify, timeout=20)


def esc(s: str) -> str:
    return html.escape(s or "")


def send_message(chat_id: int, text: str) -> None:
    try:
        _HTTP.post(
            f"{_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        )
    except Exception as e:  # noqa: BLE001
        print("telegram send_message error:", repr(e))


def typing(chat_id: int) -> None:
    try:
        _HTTP.post(
            f"{_API}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
        )
    except Exception:  # noqa: BLE001
        pass
