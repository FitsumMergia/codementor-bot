#!/bin/bash
# Run this ON THE VPS after uploading code to /opt/codementor
# Usage: bash setup_vps.sh
set -e

echo "=== CodeMentor VPS Setup ==="

cd /opt/codementor

# Python venv
if [ ! -d "venv" ]; then
    echo "[1] Creating Python environment..."
    python3 -m venv venv
fi

echo "[2] Installing dependencies..."
venv/bin/pip install -q -r requirements.txt

# Check .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: Create .env first! See DEPLOY_VPS.md Step 6"
    exit 1
fi

echo "[3] Testing bot starts..."
timeout 10 venv/bin/python -c "
from app.db import init_db
init_db()
print('DB_OK')
from app.lessons import TRACKS
print(f'Tracks: {list(TRACKS.keys())}')
print(f'Lessons: {sum(len(v) for v in TRACKS.values())}')
print('READY')
" || { echo "ERROR: Bot failed to start. Check .env"; exit 1; }

# Install systemd service
echo "[4] Installing service..."
sudo tee /etc/systemd/system/codementor.service > /dev/null << 'EOF'
[Unit]
Description=CodeMentor Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/codementor
EnvironmentFile=/opt/codementor/.env
ExecStart=/opt/codementor/venv/bin/python poll.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable codementor
sudo systemctl restart codementor
sleep 3

# Check status
if sudo systemctl is-active --quiet codementor; then
    echo ""
    echo "=== BOT IS RUNNING 24/7 ==="
    echo "Status:  sudo systemctl status codementor"
    echo "Logs:    sudo journalctl -u codementor -f"
    echo "Restart: sudo systemctl restart codementor"
else
    echo "ERROR: Service failed to start"
    sudo journalctl -u codementor --no-pager -n 20
    exit 1
fi

# Setup daily push cron
(crontab -l 2>/dev/null | grep -v daily_push; echo "0 7 * * * cd /opt/codementor && venv/bin/python daily_push.py >> /tmp/codementor_push.log 2>&1") | crontab -
echo "Daily push scheduled at 7:00 AM"
echo ""
echo "DONE! Bot is live at t.me/ByteTutorAI_Bot"
