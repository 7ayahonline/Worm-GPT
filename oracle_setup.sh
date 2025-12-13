#!/bin/bash

# 🚀 Oracle Cloud VPS - سكريبت تثبيت آلي لـ Worm GPT Bot
# هذا السكريبت سيقوم بتثبيت وتشغيل البوت على Oracle Cloud VPS

set -e  # إيقاف عند أي خطأ

echo "🔥 =========================================="
echo "🤖 Worm GPT Bot - Oracle Cloud VPS Setup"
echo "🔥 =========================================="
echo ""

# ألوان للـ Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# معلومات البوت
BOT_TOKEN="8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk"
WEBHOOK_SECRET="worm-gpt-secret-2025-secure"
BOT_DIR="/home/ubuntu/worm-gpt-bot"
SERVICE_NAME="worm-gpt-bot"

echo -e "${YELLOW}📋 معلومات الإعداد:${NC}"
echo "   📁 مجلد البوت: $BOT_DIR"
echo "   🤖 Bot Token: ${BOT_TOKEN:0:20}..."
echo "   🔐 Webhook Secret: $WEBHOOK_SECRET"
echo ""

# الحصول على Public IP للسيرفر
echo -e "${YELLOW}🌐 جاري الحصول على Public IP...${NC}"
PUBLIC_IP=$(curl -s ifconfig.me)
WEBHOOK_URL="http://${PUBLIC_IP}:5000/webhook"
echo -e "${GREEN}✅ Public IP: $PUBLIC_IP${NC}"
echo -e "${GREEN}✅ Webhook URL: $WEBHOOK_URL${NC}"
echo ""

# 1. تحديث النظام
echo -e "${YELLOW}📦 الخطوة 1/7: تحديث النظام...${NC}"
sudo apt update -qq
sudo apt upgrade -y -qq
echo -e "${GREEN}✅ تم تحديث النظام${NC}"
echo ""

# 2. تثبيت Python و pip
echo -e "${YELLOW}🐍 الخطوة 2/7: تثبيت Python 3.10...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget -qq
echo -e "${GREEN}✅ تم تثبيت Python $(python3 --version)${NC}"
echo ""

# 3. استنساخ المشروع من GitHub
echo -e "${YELLOW}📥 الخطوة 3/7: تنزيل البوت من GitHub...${NC}"
if [ -d "$BOT_DIR" ]; then
    echo "   📁 المجلد موجود بالفعل، سيتم تحديثه..."
    cd $BOT_DIR
    git pull origin master
else
    git clone https://github.com/7ayahonline/Worm-GPT.git $BOT_DIR
    cd $BOT_DIR
fi
echo -e "${GREEN}✅ تم تنزيل البوت${NC}"
echo ""

# 4. إنشاء بيئة افتراضية وتثبيت المكتبات
echo -e "${YELLOW}📦 الخطوة 4/7: تثبيت المكتبات المطلوبة...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ تم تثبيت جميع المكتبات${NC}"
echo ""

# 5. إنشاء ملف .env
echo -e "${YELLOW}⚙️ الخطوة 5/7: إعداد متغيرات البيئة...${NC}"
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
WEBHOOK_URL=$WEBHOOK_URL
WEBHOOK_SECRET=$WEBHOOK_SECRET
PORT=5000
ENVIRONMENT=production
EOF
echo -e "${GREEN}✅ تم إنشاء ملف .env${NC}"
echo ""

# 6. فتح البورت في الـ Firewall
echo -e "${YELLOW}🔓 الخطوة 6/7: فتح البورت 5000...${NC}"
sudo ufw allow 5000/tcp -q 2>/dev/null || echo "   ⚠️ UFW غير مفعّل (طبيعي في Oracle Cloud)"
echo -e "${GREEN}✅ تم فتح البورت 5000${NC}"
echo ""

# 7. إنشاء خدمة systemd
echo -e "${YELLOW}🔧 الخطوة 7/7: إنشاء خدمة systemd...${NC}"
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
echo -e "${GREEN}✅ تم إنشاء وتشغيل الخدمة${NC}"
echo ""

# انتظار 3 ثوانٍ للتأكد من بدء البوت
sleep 3

# التحقق من حالة الخدمة
echo -e "${YELLOW}🔍 التحقق من حالة البوت...${NC}"
if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
    echo -e "${GREEN}✅ البوت شغال بنجاح!${NC}"
    echo ""
    echo -e "${GREEN}🎉 =========================================="
    echo "✅ تم تثبيت البوت بنجاح!"
    echo "🔥 ==========================================${NC}"
    echo ""
    echo -e "${YELLOW}📊 معلومات مهمة:${NC}"
    echo "   🌐 Webhook URL: $WEBHOOK_URL"
    echo "   🔐 Webhook Secret: $WEBHOOK_SECRET"
    echo "   📱 Bot: @Ts_6_Bot"
    echo ""
    echo -e "${YELLOW}📝 أوامر مفيدة:${NC}"
    echo "   🔍 مراقبة البوت:    sudo systemctl status $SERVICE_NAME"
    echo "   📋 عرض اللوجات:     sudo journalctl -u $SERVICE_NAME -f"
    echo "   🔄 إعادة تشغيل:     sudo systemctl restart $SERVICE_NAME"
    echo "   🛑 إيقاف البوت:     sudo systemctl stop $SERVICE_NAME"
    echo ""
    echo -e "${GREEN}🎯 اختبر البوت الآن على Telegram: @Ts_6_Bot${NC}"
else
    echo -e "${RED}❌ فشل تشغيل البوت!${NC}"
    echo ""
    echo -e "${YELLOW}🔍 عرض الأخطاء:${NC}"
    sudo journalctl -u ${SERVICE_NAME} -n 50 --no-pager
    exit 1
fi
