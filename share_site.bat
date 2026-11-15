@echo off
title NABAS Public Tunnel
echo ========================================================
echo   Starting Cloudflare Tunnel for NABAS (127.0.0.1:8000)
echo ========================================================
echo.
echo Make sure your Django server is running in another terminal:
echo   python manage.py runserver
echo.
echo Connecting to Cloudflare edge...
echo Copy the https://xxxx.trycloudflare.com link below and share it!
echo.
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
