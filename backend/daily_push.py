"""Daily push message — run once per day (manually, cron, or Task Scheduler).

Sends each user a short motivational message + their next lesson topic.
Uses direct Telegram API calls (no AI, zero cost).

Usage:
  python daily_push.py              # send to all users
  python daily_push.py --dry-run    # preview without sending

In Phase 3, high-volume personalized daily messages move to the Gemini/Claude
Batch API (50% cost reduction). For now, these are static templates — free.
"""
import sys
import warnings

warnings.filterwarnings("ignore")

from app.config import settings
from app.db import init_db
from app.lessons import LESSONS
from app.repo import get_all_chat_ids
from app.telegram import send_message

TOTAL = len(LESSONS)

TEMPLATES = [
    "Good morning, {name}! Ready for today's Python lesson? 🐍\n\nYour next topic: <b>{topic}</b>\n\nSend /next to start.",
    "Hey {name}! Your daily coding challenge awaits 💪\n\nUp next: <b>{topic}</b>\n\nSend /next to jump in.",
    "Hi {name}! Consistency beats talent. Let's keep your streak going 🔥\n\nNext lesson: <b>{topic}</b>\n\nSend /next to continue.",
]


def main() -> None:
    init_db()
    dry_run = "--dry-run" in sys.argv

    users = get_all_chat_ids()
    print(f"{'[DRY RUN] ' if dry_run else ''}Sending daily push to {len(users)} users...")

    from datetime import date
    template = TEMPLATES[date.today().toordinal() % len(TEMPLATES)]

    sent = 0
    for user_id, chat_id, name, lesson_idx in users:
        if lesson_idx >= TOTAL:
            topic = "Review — you finished all lessons!"
        else:
            topic = LESSONS[lesson_idx]["topic"]

        msg = template.format(name=name, topic=topic)

        if dry_run:
            print(f"  [{chat_id}] {name}: {topic}")
        else:
            send_message(int(chat_id), msg)
            sent += 1

    print(f"{'Would send' if dry_run else 'Sent'} {sent if not dry_run else len(users)} messages.")


if __name__ == "__main__":
    main()
