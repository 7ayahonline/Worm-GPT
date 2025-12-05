@echo off
chcp 65001 >nul
title Worm GPT Bot - Installer
color 0A

echo.
echo ═══════════════════════════════════════════
echo    🤖 Worm GPT Bot - تثبيت المتطلبات
echo ═══════════════════════════════════════════
echo.

echo [1/3] 🔍 التحقق من Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت! قم بتثبيته أولاً.
    pause
    exit /b 1
)

echo.
echo [2/3] 📦 تثبيت المكتبات المطلوبة...
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ فشل تثبيت المكتبات!
    pause
    exit /b 1
)

echo.
echo [3/3] ✅ تم التثبيت بنجاح!
echo.
echo ═══════════════════════════════════════════
echo    ✨ جاهز للتشغيل!
echo    👉 شغل ملف run.bat لبدء البوت
echo ═══════════════════════════════════════════
echo.

pause
