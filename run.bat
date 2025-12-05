@echo off
chcp 65001 >nul
title Worm GPT Bot - Running
color 0B

:start
cls
echo.
echo ═══════════════════════════════════════════
echo    🤖 Worm GPT Bot
echo    🚀 البوت يعمل الآن...
echo ═══════════════════════════════════════════
echo.
echo 📌 معلومات البوت:
echo    • المعرف: @Ts_6_Bot
echo    • المطور: @Zi_ad_02
echo    • واتساب الدعم: +20 112 030 0273
echo.
echo ⚠️  للإيقاف: اضغط Ctrl+C
echo ═══════════════════════════════════════════
echo.

setlocal
cd /d "%~dp0"

echo Checking lock...
if exist bot.lock (
    echo Found bot.lock, removing to avoid conflicts.
    del /f /q bot.lock
)

echo Starting bot...
python bot.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ البوت توقف بسبب خطأ!
    echo 🔄 سيتم إعادة التشغيل خلال 5 ثواني...
    timeout /t 5 /nobreak >nul
    goto start
)

echo.
echo Bot stopped. Press any key to close.
pause >nul
endlocal
pause
