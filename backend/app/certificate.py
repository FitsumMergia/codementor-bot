"""Certificate generation — text-based certificate sent as a formatted message.

A visual PDF/image certificate is a Phase 6 upgrade. For now, a well-formatted
text certificate with a verification code is sufficient and costs zero.
"""
import hashlib
from datetime import date


def generate_certificate(user_name: str, track: str, total_lessons: int, user_id: int) -> tuple[str, str]:
    """Returns (certificate_text_html, verification_code)."""
    today = date.today().isoformat()
    track_name = "Python" if track == "python" else "JavaScript"

    raw = f"{user_id}-{track}-{today}-codementor"
    verify_code = "CM-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()

    cert = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "       🎓 <b>CERTIFICATE</b>\n"
        "        <b>of Completion</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "This certifies that\n\n"
        "        <b>{name}</b>\n\n"
        "has successfully completed the\n\n"
        "  <b>CodeMentor {track} Course</b>\n"
        "        ({lessons} lessons)\n\n"
        "Date: {date}\n"
        "Verification: <code>{code}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "     Issued by CodeMentor AI\n"
        "      t.me/ByteTutorAI_Bot\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ).format(
        name=user_name,
        track=track_name,
        lessons=total_lessons,
        date=today,
        code=verify_code,
    )

    return cert, verify_code
