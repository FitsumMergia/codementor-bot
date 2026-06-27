@echo off
title CodeMentor Bot - LIVE
cd /d "%~dp0"

echo ============================================
echo   CodeMentor Bot - Starting...
echo   https://t.me/ByteTutorAI_Bot
echo ============================================
echo.
echo Send /start to the bot on Telegram!
echo Press Ctrl+C to stop.
echo.

python poll.py
pause
