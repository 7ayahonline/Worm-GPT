#!/bin/bash

# 🚀 Worm GPT Bot - تشغيل تلقائي مع WinSCP
# هذا الملف سيقوم بتثبيت وتشغيل البوت على Oracle Cloud VPS

set -e

echo "🔥 =========================================="
echo "🤖 Worm GPT Bot - Quick Setup"
echo "🔥 =========================================="
echo ""

# معلومات البوت
BOT_DIR=$(pwd)
SERVICE_NAME="worm-gpt-bot"

echo "📁 مجلد البوت: $BOT_DIR"
echo ""

# الحصول على Public IP (للـ Webhook URL)
echo "🌐 جاري الحصول على Public IP..."
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "YOUR_PUBLIC_IP")
echo "✅ Public IP: $PUBLIC_IP"
echo ""

# 1. تحديث النظام
echo "📦 تحديث النظام..."
sudo apt update -qq
sudo apt upgrade -y -qq
echo "✅ تم تحديث النظام"
echo ""

# 2. تثبيت Python و pip
echo "🐍 تثبيت Python والمكتبات..."
sudo apt install -y python3 python3-pip python3-venv git curl -qq
echo "✅ تم تثبيت Python"
echo ""

# 3. إنشاء بيئة افتراضية
echo "📦 إنشاء بيئة افتراضية..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
echo "✅ تم إنشاء البيئة الافتراضية"
echo ""

# 4. تثبيت المكتبات
echo "📚 تثبيت المكتبات المطلوبة..."
pip install -r requirements.txt -q
echo "✅ تم تثبيت جميع المكتبات"
echo ""

# 5. إنشاء ملف .env
echo "⚙️ إعداد متغيرات البيئة..."
cat > .env << EOF
TELEGRAM_BOT_TOKEN=8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk
WEBHOOK_URL=http://${PUBLIC_IP}:5000/webhook
WEBHOOK_SECRET=worm-gpt-secret-2025-secure
PORT=5000
ENVIRONMENT=production
EOF
echo "✅ تم إنشاء ملف .env"
echo ""

# 6. فتح البورت في Firewall
echo "🔓 فتح البورت 5000..."
sudo ufw allow 5000/tcp -q 2>/dev/null || true
echo "✅ تم فتح البورت 5000"
echo ""

# 7. إنشاء خدمة systemd
echo "🔧 إنشاء خدمة systemd..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOF
[Unit]
Description=Worm GPT Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$BOT_DIR
Environment="PATH=$BOT_DIR/venv/bin"
EnvironmentFile=$BOT_DIR/.env
ExecStart=$BOT_DIR/venv/bin/python bot_webhook.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl start ${SERVICE_NAME}
echo "✅ تم إنشاء الخدمة"
echo ""

# انتظار 3 ثوانٍ
sleep 3

# التحقق من حالة الخدمة
echo "🔍 التحقق من حالة البوت..."
if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
    echo "✅ البوت شغال بنجاح!"
    echo ""
    echo "🎉 =========================================="
    echo "✅ تم التثبيت بنجاح!"
    echo "🎉 =========================================="
    echo ""
    echo "📊 معلومات مهمة:"
    echo "   🌐 Public IP: $PUBLIC_IP"
    echo "   🔗 Webhook URL: http://${PUBLIC_IP}:5000/webhook"
    echo "   📱 Bot: @Ts_6_Bot"
    echo ""
    echo "📝 أوامر مفيدة:"
    echo "   حالة البوت:     sudo systemctl status worm-gpt-bot"
    echo "   عرض اللوجات:    sudo journalctl -u worm-gpt-bot -f"
    echo "   إعادة تشغيل:    sudo systemctl restart worm-gpt-bot"
    echo "   إيقاف البوت:    sudo systemctl stop worm-gpt-bot"
    echo ""
else
    echo "❌ فشل تشغيل البوت!"
    echo ""
    echo "🔍 عرض الأخطاء:"
    sudo journalctl -u ${SERVICE_NAME} -n 50 --no-pager
    exit 1
fi
