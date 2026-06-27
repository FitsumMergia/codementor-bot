@echo off
title CodeMentor Tunnel
echo Starting ngrok tunnel to port 8000...
echo Copy the https URL from the output below and paste it when prompted.
echo.
ngrok http 8000
