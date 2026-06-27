#!/bin/bash
# CodeMentor VPS deployment script
# Run on a fresh Ubuntu 22.04+ VPS as root:
#   curl -sL https://raw.githubusercontent.com/.../deploy.sh | bash
# Or copy this file to the VPS and run: bash deploy.sh

set -e

echo "=== CodeMentor Bot — VPS Setup ==="

# 1. System deps
echo "[1/6] Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip git

# 2. Create user
echo "[2/6] Creating codementor user..."
id codementor &>/dev/null || useradd -m -s /bin/bash codementor

# 3. Deploy code
echo "[3/6] Deploying code to /opt/codementor..."
mkdir -p /opt/codementor
cp -r app/ poll.py daily_push.py requirements.txt /opt/codementor/
chown -R codementor:codementor /opt/codementor

# 4. Python venv
echo "[4/6] Setting up Python environment..."
sudo -u codementor python3 -m venv /opt/codementor/venv
sudo -u codementor /opt/codementor/venv/bin/pip install -q -r /opt/codementor/requirements.txt

# 5. .env file
if [ ! -f /opt/codementor/.env ]; then
    echo "[5/6] Creating .env template..."
    cat > /opt/codementor/.env << 'ENVEOF'
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_SECRET_TOKEN=cm-phase1-xK9mP2vR7wQ4nL6j
GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE
ANTHROPIC_API_KEY=
DATABASE_URL=sqlite:///./codementor.db
ADMIN_TOKEN=cm-admin-bT5yH8kN3rW1mX6p
ADMIN_CHAT_ID=
SSL_VERIFY=true
ENVEOF
    chown codementor:codementor /opt/codementor/.env
    chmod 600 /opt/codementor/.env
    echo ">>> EDIT /opt/codementor/.env with your real tokens! <<<"
else
    echo "[5/6] .env already exists, keeping it."
fi

# 6. Systemd service
echo "[6/6] Installing systemd service..."
cp codementor.service /etc/systemd/system/codementor.service
systemctl daemon-reload
systemctl enable codementor
systemctl start codementor

echo ""
echo "=== DONE ==="
echo "Bot status:  systemctl status codementor"
echo "Bot logs:    journalctl -u codementor -f"
echo "Restart:     systemctl restart codementor"
echo "Edit config: nano /opt/codementor/.env && systemctl restart codementor"
echo ""
echo ">>> Don't forget to edit /opt/codementor/.env with your real tokens! <<<"
