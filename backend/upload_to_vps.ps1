# Upload CodeMentor to VPS
# Edit these two lines, then run: powershell -File upload_to_vps.ps1

$KEY = "C:\Users\fitsum.mergia\Downloads\ssh-key.key"   # Path to your SSH private key
$VPS = "ubuntu@YOUR_VPS_IP"                               # Replace YOUR_VPS_IP

$SRC = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "=== Uploading CodeMentor to VPS ===" -ForegroundColor Cyan

# Create directory on VPS
ssh -i $KEY $VPS "mkdir -p /opt/codementor/app"

# Upload code
Write-Host "Uploading app code..."
scp -i $KEY -r "$SRC\app\*.py" "${VPS}:/opt/codementor/app/"
scp -i $KEY "$SRC\poll.py" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\daily_push.py" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\requirements.txt" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\setup_vps.sh" "${VPS}:/opt/codementor/"
scp -i $KEY "$SRC\.env" "${VPS}:/opt/codementor/"

Write-Host ""
Write-Host "=== Upload complete ===" -ForegroundColor Green
Write-Host "Now SSH in and run the setup:"
Write-Host "  ssh -i $KEY $VPS"
Write-Host "  cd /opt/codementor && bash setup_vps.sh"
