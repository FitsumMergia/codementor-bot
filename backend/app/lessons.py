"""Multi-track lesson system.

Tracks:
  - python    : 30 lessons (15 beginner + 15 intermediate)
  - javascript: 15 lessons

The active track is stored per-user in the sessions table.
LESSONS is the default (Python) for backward compatibility.
"""
from .lessons_python_beginner import LESSONS_PYTHON_BEGINNER
from .lessons_python_intermediate import LESSONS_PYTHON_INTERMEDIATE
from .lessons_javascript import LESSONS_JAVASCRIPT

TRACKS = {
    "python": LESSONS_PYTHON_BEGINNER + LESSONS_PYTHON_INTERMEDIATE,
    "javascript": LESSONS_JAVASCRIPT,
}

TRACK_INFO = {
    "python": {"name": "Python", "emoji": "🐍", "lessons": len(TRACKS["python"])},
    "javascript": {"name": "JavaScript", "emoji": "🟨", "lessons": len(TRACKS["javascript"])},
}

# Default track for backward compatibility
LESSONS = TRACKS["python"]


def get_track_lessons(track: str) -> list[dict]:
    return TRACKS.get(track, LESSONS)
