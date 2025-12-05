# 🚀 دليل النشر على الاستضافة

## الخوادم المدعومة:
- ✅ Linux Servers
- ✅ cPanel Hosting
- ✅ Shared Hosting
- ✅ VPS
- ✅ Dedicated Servers

---

## 📋 المتطلبات:

```
Python 3.8+
pip (Python Package Manager)
```

---

## 🔧 خطوات التثبيت على الاستضافة:

### 1️⃣ الاتصال بـ SSH

```bash
ssh your_username@7ayahonline.com
# ادخل كلمة المرور
```

### 2️⃣ نسخ المشروع

**الطريقة أ: من Git**
```bash
cd public_html
git clone <your-github-repo-url>
cd worm-gpt-bot
```

**الطريقة ب: من ملف مضغوط**
```bash
cd public_html
unzip bot.zip
cd بوت\ worm\ gpt
```

**الطريقة ج: عبر FTP**
رفع الملفات يدويًا إلى `/public_html/`

### 3️⃣ تثبيت المتطلبات

```bash
pip install -r requirements.txt
# أو
pip3 install -r requirements.txt
```

### 4️⃣ إعداد متغيرات البيئة

```bash
# أنشئ ملف .env
nano .env
```

أضف المتغيرات التالية:
```env
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
TELEGRAM_BOT_ID=YOUR_BOT_ID
ADMIN_IDS=YOUR_ADMIN_ID
PAYPAL_CLIENT_ID=YOUR_PAYPAL_ID
PAYPAL_SECRET=YOUR_PAYPAL_SECRET
PAYPAL_ENV=production
PAYPAL_ME_LINK=https://www.paypal.me/yourname
```

اضغط `Ctrl+X` ثم `Y` ثم `Enter` للحفظ

### 5️⃣ بدء البوت

**الطريقة أ: تشغيل مباشر**
```bash
python bot.py
```

**الطريقة ب: تشغيل في الخلفية (Nohup)**
```bash
nohup python bot.py > bot.log 2>&1 &
```

**الطريقة ج: استخدام Screen**
```bash
screen -S worm-gpt
python bot.py
# اضغط Ctrl+A ثم D للخروج مع البقاء مشغولاً
```

**الطريقة د: استخدام systemd (الأفضل)**

أنشئ ملف الخدمة:
```bash
sudo nano /etc/systemd/system/worm-gpt.service
```

أضف:
```ini
[Unit]
Description=Worm GPT Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/public_html/worm-gpt-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

ثم:
```bash
sudo systemctl daemon-reload
sudo systemctl start worm-gpt
sudo systemctl enable worm-gpt
```

---

## 📊 مراقبة البوت

### التحقق من الحالة:
```bash
# إذا كنت تستخدم systemd
sudo systemctl status worm-gpt

# إذا كنت تستخدم nohup
tail -f bot.log
```

### إيقاف البوت:
```bash
# إذا كان مشغول في Terminal
Ctrl+C

# إذا كنت تستخدم systemd
sudo systemctl stop worm-gpt

# إذا كان في screen
screen -S worm-gpt -X quit
```

### تحديث البوت:
```bash
git pull origin main
python bot.py
```

---

## 🔒 أمان الملفات

تأكد من الأذونات:
```bash
# لا تجعل bot.py قابل للتنفيذ للعامة
chmod 700 bot.py

# حماية الملفات الحساسة
chmod 600 .env
chmod 600 bot_stats.json
chmod 600 users_data.json
chmod 600 admin_actions.json
chmod 600 coupons.json
```

---

## 🐛 استكشاف الأخطاء

### لا يعمل الاتصال:
```bash
# تحقق من التوكن
grep "TELEGRAM_BOT_TOKEN" .env

# اختبر الاتصال
python -c "import requests; print(requests.get('https://api.telegram.org/botTOKEN/getMe').json())"
```

### المكتبات ناقصة:
```bash
pip install --upgrade -r requirements.txt
```

### مشاكل الترميز:
```bash
# إذا كانت هناك مشاكل مع النصوص العربية
export PYTHONIOENCODING=utf-8
python bot.py
```

---

## 📈 الأداء والتحسين

### استخدام gunicorn (للـ Web):
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 bot:app
```

### استخدام supervisor (للمراقبة):
```bash
sudo apt-get install supervisor
sudo nano /etc/supervisor/conf.d/worm-gpt.conf
```

أضف:
```ini
[program:worm-gpt]
command=/usr/bin/python3 /home/user/public_html/bot.py
directory=/home/user/public_html
autostart=true
autorestart=true
stderr_logfile=/var/log/worm-gpt.err.log
stdout_logfile=/var/log/worm-gpt.out.log
```

---

## 📞 الدعم

إذا واجهت مشاكل:
1. تحقق من `bot.log`
2. اقرأ `CONFIGURATION.md`
3. تواصل مع: @Zi_ad_02 أو +20 112 030 0273

---

**تم بنجاح! البوت يعمل الآن على الاستضافة! 🎉**
