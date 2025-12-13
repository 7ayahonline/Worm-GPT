# 🚀 WinSCP - تشغيل البوت بـ Drag & Drop

## 📋 المتطلبات
- ✅ سيرفر Oracle شغال (Ubuntu 22.04)
- ✅ Public IP من Oracle (مثل: 158.179.12.34)
- ✅ SSH Private Key (الملف اللي حملته من Oracle)
- ✅ ملفات البوت على جهازك

---

## 📥 الخطوة 1: تحميل WinSCP

**اضغط هنا:**
```
https://winscp.net/eng/download.php
```

**اختر:**
- ❌ **Portable** (لا يحتاج تثبيت)
- ✅ **Installation Package** (الأفضل)

---

## 🔌 الخطوة 2: الاتصال بالسيرفر

### أ) افتح WinSCP

```
ستشوف نافذة تسجيل الدخول
```

### ب) املأ البيانات

| الحقل | القيمة |
|------|--------|
| **File protocol** | SFTP |
| **Host name** | `YOUR_PUBLIC_IP` (مثل: 158.179.12.34) |
| **Port** | `22` |
| **Username** | `ubuntu` |
| **Password** | (اتركه فاضي) |
| **Private key file** | اختر ملف المفتاح (ssh-key-*.key) |

### ج) اضغط "Login"

```
✅ يجب أن تدخل على السيرفر مباشرة
```

---

## 📂 الخطوة 3: سحب وإفلات الملفات

### شكل البرنامج:

```
┌─────────────────────────────────────────┐
│           WinSCP Interface              │
├──────────────────┬──────────────────────┤
│  Local Files     │  Remote Files        │
│  (جهازك)         │  (السيرفر)           │
│                  │                      │
│ 📁 Desktop       │ 📁 /home/ubuntu      │
│ 📁 Downloads     │ 📁 .ssh              │
│ 📁 وورم جي بي تي │ (ملفات أخرى)        │
│ └─ ملفات البوت   │                      │
└──────────────────┴──────────────────────┘
```

### الخطوات:

1. **في الناحية اليسرى** (جهازك):
   - ابحث عن مجلد البوت
   ```
   d:\ذياد\مشاريع\بوت worm gpt
   ```

2. **اسحب المجلد كامل**:
   - اختر المجلد
   - اسحبه للناحية اليمنى (السيرفر)
   - ضعه في `/home/ubuntu/`

3. **انتظر الرفع**:
   ```
   سيظهر شريط تقدم
   ✅ بعد الانتهاء، المجلد هيبقى موجود في السيرفر
   ```

4. **التحقق**:
   ```
   في اليمين ستشوف:
   /home/ubuntu/وورم-جي-بي-تي (أو Worm-GPT)
   ├── bot_webhook.py
   ├── requirements.txt
   ├── users_data.json
   ├── bot_stats.json
   └── ملفات أخرى...
   ```

---

## 🚀 الخطوة 4: تشغيل البوت (أمر واحد!)

### أ) افتح Terminal في WinSCP

**في WinSCP:**
```
قائمة Commands → Open Terminal
```

أو **اضغط Ctrl+T**

---

### ب) نفّذ الأوامر:

```bash
# الانتقال لمجلد البوت
cd ~/Worm-GPT

# أو لو اسمه مختلف:
cd ~/وورم-جي-بي-تي

# تشغيل سكريبت التثبيت
bash setup_winscp.sh
```

**ستشوف:**
```
🔥 ==========================================
🤖 Worm GPT Bot - Quick Setup
🔥 ==========================================

📦 تحديث النظام...
✅ تم تحديث النظام

🐍 تثبيت Python والمكتبات...
✅ تم تثبيت Python

📦 إنشاء بيئة افتراضية...
✅ تم إنشاء البيئة الافتراضية

📚 تثبيت المكتبات المطلوبة...
✅ تم تثبيت جميع المكتبات

⚙️ إعداد متغيرات البيئة...
✅ تم إنشاء ملف .env

🔓 فتح البورت 5000...
✅ تم فتح البورت 5000

🔧 إنشاء خدمة systemd...
✅ تم إنشاء الخدمة

✅ البوت شغال بنجاح!

🎉 ==========================================
✅ تم التثبيت بنجاح!
🎉 ==========================================

📊 معلومات مهمة:
   🌐 Public IP: 158.179.12.34
   🔗 Webhook URL: http://158.179.12.34:5000/webhook
   📱 Bot: @Ts_6_Bot

📝 أوامر مفيدة:
   حالة البوت:     sudo systemctl status worm-gpt-bot
   عرض اللوجات:    sudo journalctl -u worm-gpt-bot -f
   إعادة تشغيل:    sudo systemctl restart worm-gpt-bot
   إيقاف البوت:    sudo systemctl stop worm-gpt-bot
```

---

## ⚠️ مهم جداً: فتح البورت 5000 في Oracle Cloud

**بدون هذه الخطوة، الـ Webhook مش هيتصل!**

1. **ارجع لـ Oracle Cloud Dashboard**

2. **اذهب إلى:**
   ```
   Menu ☰ → Networking → Virtual Cloud Networks
   ```

3. **اختر الـ VCN** الخاص بالـ Instance

4. **Security Lists → Default Security List**

5. **Add Ingress Rules:**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Destination Port Range: 5000
   Description: Telegram Webhook
   ```

6. **اضغط Add Ingress Rules**

---

## ✅ النتيجة

بعد كل شيء:

```
✅ البوت شغال 24 ساعة على Oracle VPS
✅ سحب وإفلات بسيط (بدون GitHub)
✅ بدون أوامر معقدة
✅ بدون ترك اللابتوب
✅ مجاني مدى الحياة
```

---

## 🔍 اختبر البوت

افتح Telegram:
```
ابحث عن: @Ts_6_Bot
اكتب: /start
```

**يجب أن يرد فوراً! ✅**

---

## 📝 أوامر مفيدة للمستقبل

```bash
# مراقبة البوت
sudo systemctl status worm-gpt-bot

# عرض آخر 100 سطر من اللوجات
sudo journalctl -u worm-gpt-bot -n 100

# متابعة اللوجات الحية (Real-time)
sudo journalctl -u worm-gpt-bot -f

# إعادة تشغيل البوت
sudo systemctl restart worm-gpt-bot

# إيقاف البوت
sudo systemctl stop worm-gpt-bot

# تشغيل البوت
sudo systemctl start worm-gpt-bot
```

---

## 🐛 حل المشاكل

### ❌ "No such file or directory"
```bash
# تأكد من اسم مجلد البوت
ls ~

# ثم
cd ~/اسم_المجلد_الصحيح
bash setup_winscp.sh
```

### ❌ "Permission denied"
```bash
chmod +x setup_winscp.sh
bash setup_winscp.sh
```

### ❌ "Bot is not running"
```bash
# عرض الأخطاء
sudo journalctl -u worm-gpt-bot -n 50
```

### ❌ "Bot responds but Telegram shows no updates"
1. تأكد من فتح البورت 5000 في Oracle Security List
2. اختبر الـ Webhook URL في المتصفح:
   ```
   http://YOUR_PUBLIC_IP:5000/health
   ```
   يجب أن يرد JSON بـ `{"status": "healthy", ...}`

---

## 📞 الدعم
- **Telegram:** @Zi_ad_02
- **WhatsApp:** +20 112 030 0273

---

## 🎉 تمام! البوت شغال 24/7 بسهولة!
