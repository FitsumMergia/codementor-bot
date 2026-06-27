#!/bin/bash
# CodeMentor — PythonAnywhere deployment
# Paste this ENTIRE script into a PythonAnywhere Bash console.
# It creates all files and starts the bot.

set -e
echo "=== CodeMentor PythonAnywhere Setup ==="

cd ~
rm -rf codementor 2>/dev/null
mkdir -p codementor/app
cd codementor

# 1. Virtual environment
echo "[1/4] Creating Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -q fastapi uvicorn anthropic pydantic-settings sqlalchemy pymysql httpx

# 2. Create .env
echo "[2/4] Creating config..."
cat > .env << 'ENVEOF'
TELEGRAM_BOT_TOKEN=8142307729:AAFK7ZnrMzkXxzpb496zJZq36Kh2P50n9aU
TELEGRAM_SECRET_TOKEN=cm-phase1-xK9mP2vR7wQ4nL6j
GEMINI_API_KEY=AQ.Ab8RN6IE2HSXVCSTq3CUlsgrZpr5Ma5rRDjbA7jrApf8hjARSg
ANTHROPIC_API_KEY=
DATABASE_URL=sqlite:///./codementor.db
ADMIN_TOKEN=cm-admin-bT5yH8kN3rW1mX6p
ADMIN_CHAT_ID=5088756568
SSL_VERIFY=true
ENVEOF

echo "[3/4] Creating application files..."
