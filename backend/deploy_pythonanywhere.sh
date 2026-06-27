#!/bin/bash
# ============================================================
# CodeMentor — PythonAnywhere Deployment
# ============================================================
# 1. Go to https://www.pythonanywhere.com — sign up (free, no card)
# 2. Open a Bash console
# 3. Paste this ENTIRE script and press Enter
# ============================================================

set -e
echo "=== CodeMentor PythonAnywhere Setup ==="

cd ~

# 1. Clone from GitHub
echo "[1/5] Cloning code..."
rm -rf codementor 2>/dev/null
git clone https://github.com/FitsumMergia/codementor-bot.git codementor
cd codementor/backend

# 2. Python venv
echo "[2/5] Setting up Python..."
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

# 3. Create .env with your tokens
echo "[3/5] Creating config..."
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=8142307729:AAFK7ZnrMzkXxzpb496zJZq36Kh2P50n9aU
TELEGRAM_SECRET_TOKEN=cm-phase1-xK9mP2vR7wQ4nL6j
GEMINI_API_KEY=AQ.Ab8RN6IE2HSXVCSTq3CUlsgrZpr5Ma5rRDjbA7jrApf8hjARSg
ANTHROPIC_API_KEY=
DATABASE_URL=sqlite:///./codementor.db
ADMIN_TOKEN=cm-admin-bT5yH8kN3rW1mX6p
ADMIN_CHAT_ID=5088756568
SSL_VERIFY=true
EOF

# 4. Initialize DB
echo "[4/5] Initializing database..."
python -c "from app.db import init_db; init_db(); print('DB OK')"
python -c "from app.lessons import TRACKS; print(f'Tracks: {list(TRACKS.keys())}, Lessons: {sum(len(v) for v in TRACKS.values())}')"

# 5. Done
echo ""
echo "============================================================"
echo "  SETUP COMPLETE!"
echo ""
echo "  To start the bot, run:"
echo "    cd ~/codementor/backend"
echo "    source venv/bin/activate"
echo "    python poll.py"
echo ""
echo "  Bot URL: https://t.me/ByteTutorAI_Bot"
echo ""
echo "  NOTE: PythonAnywhere free tier keeps consoles"
echo "  open for ~3 hours. Restart anytime with:"
echo "    cd ~/codementor/backend && source venv/bin/activate && python poll.py"
echo "============================================================"
