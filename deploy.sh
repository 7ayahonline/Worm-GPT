#!/bin/bash
# 🚀 نشر تلقائي على Render
# Automated Deployment Script for Render

set -e  # Exit on error

echo "🚀 بدء النشر على Render..."
echo "📦 تثبيت المتطلبات..."

# تثبيت المتطلبات
pip install -q -r requirements.txt

echo "✅ تم تثبيت المتطلبات"
echo "🧪 اختبار الكود..."

# اختبار صحة الكود
python -m py_compile bot_webhook.py

echo "✅ الكود صحيح"
echo "🌐 بدء البوت..."

# تشغيل البوت
python bot_webhook.py
