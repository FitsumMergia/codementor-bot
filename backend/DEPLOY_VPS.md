# Deploy CodeMentor Bot to Oracle Cloud (Free Forever)

Oracle Cloud gives you a free VM that never expires — perfect for running the bot 24/7.

---

## Step 1: Create Oracle Cloud Account (5 min)

1. Go to **https://cloud.oracle.com/sign-up**
2. Sign up with your email (fitsummergia@gmail.com)
3. Choose region: **pick the closest** (e.g., South Africa or UK)
4. You need a credit/debit card for verification — **it will NOT be charged**
5. Complete sign-up, verify email

**No card?** Use **PythonAnywhere** instead (free, no card needed):
- Go to https://www.pythonanywhere.com
- Sign up free → open a Bash console → follow the "Alternative" section at the bottom of this guide

---

## Step 2: Create a Free VM (3 min)

1. Login to **https://cloud.oracle.com**
2. Click **"Create a VM instance"** (on the dashboard)
3. Configure:
   - **Name:** `codementor`
   - **Image:** Ubuntu 22.04 (default)
   - **Shape:** Click "Change shape" → **Ampere** → **VM.Standard.A1.Flex** → 1 OCPU, 1 GB RAM
   - **SSH Key:** Click "Generate a key pair" → **Download both keys** (save them!)
4. Click **Create**
5. Wait ~2 min for it to boot
6. Copy the **Public IP Address** shown on the instance page

---

## Step 3: Connect to your VM (2 min)

Open a terminal (PowerShell on Windows):

```powershell
# Replace with YOUR key file path and IP
ssh -i "C:\Users\fitsum.mergia\Downloads\ssh-key.key" ubuntu@YOUR_IP_HERE
```

If it asks about fingerprint, type `yes`.

**Windows tip:** If the key file gives a permissions error:
```powershell
icacls "C:\Users\fitsum.mergia\Downloads\ssh-key.key" /reset
icacls "C:\Users\fitsum.mergia\Downloads\ssh-key.key" /grant:r "%username%:R"
icacls "C:\Users\fitsum.mergia\Downloads\ssh-key.key" /inheritance:r
```

---

## Step 4: Deploy the bot (3 min)

Once connected via SSH, run these commands ONE BY ONE:

```bash
# 1. Install Python
sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-venv python3-pip

# 2. Create app directory
sudo mkdir -p /opt/codementor
sudo chown $USER:$USER /opt/codementor
cd /opt/codementor

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi>=0.110
uvicorn[standard]>=0.27
anthropic>=0.49
pydantic>=2.6
pydantic-settings>=2.2
SQLAlchemy>=2.0
PyMySQL>=1.1
httpx>=0.27
EOF

# 5. Install dependencies
pip install -q -r requirements.txt
```

---

## Step 5: Upload your code (2 min)

**Option A — Copy/paste (simplest):**

Still on the VPS via SSH:

```bash
cd /opt/codementor

# Create the app directory structure
mkdir -p app

# Now use this one-liner to download your code:
# (You'll paste each file — I'll provide a script below)
```

**Option B — Use the upload script (recommended):**

On your LOCAL PC (not the VPS), open a NEW terminal and run:

```powershell
# Replace KEY_PATH and VPS_IP with your values
$KEY = "C:\Users\fitsum.mergia\Downloads\ssh-key.key"
$VPS = "ubuntu@YOUR_IP_HERE"
$SRC = "D:\02_Projects\AI\Co-work\CodeMentor Chat AI\backend"

# Upload all files
scp -i $KEY -r "$SRC\app" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\poll.py" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\daily_push.py" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\requirements.txt" "${VPS}:/opt/codementor/"
```

---

## Step 6: Configure secrets (1 min)

Back on the VPS via SSH:

```bash
cd /opt/codementor

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

chmod 600 .env
```

---

## Step 7: Test it works (1 min)

```bash
cd /opt/codementor
source venv/bin/activate
python poll.py
```

You should see:
```
CodeMentor Bot
https://t.me/ByteTutorAI_Bot
Listening...
```

Send `/start` to the bot on Telegram. If it responds, press **Ctrl+C** to stop (we'll set it up as a service next).

---

## Step 8: Run forever as a service (2 min)

```bash
# Create systemd service
sudo tee /etc/systemd/system/codementor.service << 'EOF'
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

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable codementor
sudo systemctl start codementor

# Check it's running
sudo systemctl status codementor
```

---

## Step 9: Open the firewall (Oracle-specific)

Oracle blocks all incoming traffic by default. For the bot (polling mode) this doesn't matter — it makes outbound connections only. But if you want the landing page or webhook later:

```bash
# Open port 80 and 443
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

Also add these in the Oracle Cloud Console:
1. Go to **Networking → Virtual Cloud Networks** → your VCN
2. Click **Security Lists** → **Default Security List**
3. Add **Ingress Rule**: Source `0.0.0.0/0`, TCP, Port `80`
4. Add **Ingress Rule**: Source `0.0.0.0/0`, TCP, Port `443`

---

## Useful commands

```bash
# Check bot status
sudo systemctl status codementor

# View live logs
sudo journalctl -u codementor -f

# Restart bot (after code changes)
sudo systemctl restart codementor

# Stop bot
sudo systemctl stop codementor

# Update code (from your local PC)
scp -i KEY -r backend/app ubuntu@IP:/opt/codementor/
scp -i KEY backend/poll.py ubuntu@IP:/opt/codementor/
ssh -i KEY ubuntu@IP "sudo systemctl restart codementor"

# Daily push (add to crontab)
crontab -e
# Add: 0 7 * * * cd /opt/codementor && venv/bin/python daily_push.py
```

---

## Alternative: PythonAnywhere (no card needed)

If you can't get Oracle Cloud (needs a card):

1. Go to **https://www.pythonanywhere.com** → Sign up (free, no card)
2. Open a **Bash console**
3. Run:

```bash
cd ~
mkdir codementor && cd codementor
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn anthropic pydantic-settings sqlalchemy pymysql httpx

# Create files (paste each file's content)
mkdir app
# ... paste each file using nano or the built-in editor

# Create .env with your tokens
nano .env

# Run
python poll.py
```

**PythonAnywhere free tier limitation:** The console closes after ~3 hours of inactivity. Upgrade to $5/month "Hacker" plan for always-on tasks. Still cheaper than any VPS.

---

## Cost summary

| Provider | Monthly | Always-on | Card needed |
|----------|---------|-----------|-------------|
| Oracle Cloud Free | $0 forever | Yes | Yes (verify only) |
| PythonAnywhere Free | $0 | No (3hr limit) | No |
| PythonAnywhere Hacker | $5/mo | Yes | Yes |
| Hetzner VPS | $3.29/mo | Yes | Yes |
