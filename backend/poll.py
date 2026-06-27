"""Long-polling mode — no tunnel needed.

Run:  python poll.py

Press Ctrl+C to stop. Only ONE instance can run at a time.
"""
import time
import sys
import warnings
import httpx

warnings.filterwarnings("ignore")

from app.config import settings
from app.db import init_db
from app.bot import handle_update

BOT_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}"
_HTTP = httpx.Client(verify=settings.ssl_verify, timeout=40)


def clear_webhook() -> None:
    """Delete webhook and drop pending updates to clear any 409 conflicts."""
    r = _HTTP.post(f"{BOT_API}/deleteWebhook", json={"drop_pending_updates": True})
    print(f"deleteWebhook -> {r.json().get('ok')}", flush=True)
    # Make a short getUpdates call to claim the polling slot
    try:
        _HTTP.get(f"{BOT_API}/getUpdates", params={"offset": -1, "timeout": 1})
    except Exception:
        pass
    time.sleep(1)


def poll_forever() -> None:
    offset = 0
    print(flush=True)
    print("=" * 50, flush=True)
    print("  CodeMentor Bot", flush=True)
    print("  https://t.me/ByteTutorAI_Bot", flush=True)
    print("=" * 50, flush=True)
    print(flush=True)
    print("Listening... (Ctrl+C to stop)", flush=True)

    consecutive_errors = 0

    while True:
        try:
            r = _HTTP.get(
                f"{BOT_API}/getUpdates",
                params={"offset": offset, "timeout": 30, "allowed_updates": '["message"]'},
            )
            data = r.json()

            if not data.get("ok"):
                err_code = data.get("error_code")
                err_desc = data.get("description", "")

                if err_code == 409:
                    print("409 conflict — another instance running. Retrying in 5s...", flush=True)
                    consecutive_errors += 1
                    if consecutive_errors >= 3:
                        print("Still conflicting. Clearing with deleteWebhook...", flush=True)
                        clear_webhook()
                        consecutive_errors = 0
                    time.sleep(5)
                    continue

                print(f"getUpdates error: {data}", flush=True)
                time.sleep(5)
                continue

            consecutive_errors = 0

            for update in data.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                who = msg.get("from", {}).get("first_name", "?")
                text = (msg.get("text") or "")[:50]
                print(f"  [{who}] {text}", flush=True)
                try:
                    handle_update(update)
                except Exception as e:
                    print(f"  ERROR: {e}", flush=True)

        except httpx.TimeoutException:
            pass
        except KeyboardInterrupt:
            print("\nStopping...", flush=True)
            break
        except Exception as e:
            print(f"Poll error: {e}", flush=True)
            time.sleep(5)


def main() -> None:
    init_db()
    clear_webhook()
    poll_forever()


if __name__ == "__main__":
    main()
