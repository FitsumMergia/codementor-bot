@echo off
title CodeMentor Backend
cd /d "%~dp0"
echo Starting CodeMentor backend on port 8000...
echo Press Ctrl+C to stop.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
