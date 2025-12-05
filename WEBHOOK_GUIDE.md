# 🚀 دليل نشر البوت بـ Webhook (24/7)

## ❓ الفرق بين Polling و Webhook

### ❌ Polling (القديم):
```
البوت يسأل Telegram كل 3 ثوان: "في رسائل ليا؟"
└─ استهلاك موارد عالي
└─ بطيء في الاستجابة
└─ يتوقف عند إغلاق اللابتوب
```

### ✅ Webhook (الجديد):
```
Telegram يرسل الرسائل مباشرة للبوت
└─ استهلاك موارد قليل
└─ استجابة فورية
└─ يعمل 24/7 على السحابة
└─ حتى لو أطفأت اللابتوب! ✨
```

---

## 📦 الملفات الجديدة:

```
bot_webhook.py      ← البوت الجديد (Webhook mode)
requirements.txt    ← محدّث (Flask, gunicorn)
Procfile           ← سكريبت Render
render.yaml        ← إعدادات Render
```

---

## 🔧 الإعدادات المطلوبة:

### متغيرات البيئة:

```env
# الضروري:
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
WEBHOOK_URL=https://your-domain.onrender.com/webhook
WEBHOOK_SECRET=your-secret-key

# اختياري:
PAYPAL_CLIENT_ID=...
PAYPAL_SECRET=...
PAYPAL_ENV=sandbox
PAYPAL_ME_LINK=...
PORT=5000
```

---

## 🌐 الخطوات على Render:

### 1️⃣ إنشاء Web Service
```
Dashboard → + New → Web Service
```

### 2️⃣ ربط GitHub
```
Repository: https://github.com/7ayahonline/Worm-GPT.git
Branch: master
Build Command: pip install -r requirements.txt
Start Command: python bot_webhook.py
```

### 3️⃣ متغيرات البيئة
```
Environment Variables:
├─ TELEGRAM_BOT_TOKEN = (من @BotFather)
├─ WEBHOOK_URL = https://your-service.onrender.com/webhook
├─ WEBHOOK_SECRET = your-secret-key
├─ PAYPAL_CLIENT_ID = (اختياري)
└─ PAYPAL_SECRET = (اختياري)
```

### 4️⃣ النشر
```
Create Web Service → انتظر الإكمال
```

### 5️⃣ الحصول على رابط الـ Webhook
```
Dashboard → Service → Settings
البحث عن: Service URL (مثل: https://xxx.onrender.com)
```

### 6️⃣ تحديث WEBHOOK_URL
```
Environment Variables → WEBHOOK_URL
الرابط: https://xxx.onrender.com/webhook
Save & Deploy
```

---

## 🧪 الاختبار المحلي:

### تشغيل البوت محلياً (للاختبار):

```bash
# اذهب إلى المجلد
cd "d:\ذياد\مشاريع\بوت worm gpt"

# شغّل البوت
python bot_webhook.py
```

### سيظهر:
```
🤖 البوت يعمل الآن على المنفذ 5000 (Webhook mode)
```

### في متصفح:
```
http://localhost:5000/
```

سترى:
```json
{
  "status": "running",
  "bot": "Worm GPT Bot",
  "version": "3.0.1",
  "mode": "Webhook"
}
```

---

## 🔄 كيفية التبديل من Polling إلى Webhook:

### قبل (bot.py - Polling):
```python
# الملف: bot.py
# يستخدم: getUpdates كل 3 ثوانٍ
# يتوقف عند إغلاق اللابتوب ❌
```

### الآن (bot_webhook.py - Webhook):
```python
# الملف: bot_webhook.py
# يستخدم: setWebhook + Flask
# يعمل 24/7 على السحابة ✅
```

---

## 📱 كيفية يعمل Webhook:

```
1. البوت يخبر Telegram: "أرسل الرسائل لـ https://my-bot.com/webhook"
2. المستخدم يرسل رسالة
3. Telegram يرسلها مباشرة للبوت
4. البوت يرد فوراً ✅
```

---

## 🔒 الأمان:

### WEBHOOK_SECRET:
```
تحقق أن الطلب من Telegram فقط (ليس من أي حد ثاني)

Header: X-Telegram-Bot-Api-Secret-Token
Value: your-secret-key
```

---

## 📊 معايير الأداء:

| المعيار | Polling | Webhook |
|--------|---------|---------|
| **الاستجابة** | 1-3 ثوانٍ | فوري (< 100ms) |
| **استهلاك CPU** | عالي | منخفض |
| **استهلاك Memory** | 100+ MB | 30-50 MB |
| **عدد الطلبات** | 28,800/يوم | حسب الاستخدام |
| **24/7** | ❌ | ✅ |

---

## 🚀 النشر على Render بـ Webhook:

### قبل النشر:
```bash
1. تحديث WEBHOOK_URL في متغيرات البيئة
2. تحديث WEBHOOK_SECRET
3. Test محلي: python bot_webhook.py
4. Push على GitHub
```

### بعد النشر:
```bash
1. Bot سيكون متاح على: https://your-service.onrender.com
2. Webhook سيكون: https://your-service.onrender.com/webhook
3. يعمل 24/7 (في الخطة المدفوعة)
```

---

## ⚙️ المنافذ:

```
المحلي (Localhost):
http://localhost:5000/webhook

الإنتاج (Render):
https://your-service.onrender.com/webhook
```

---

## 🔍 استكشاف الأخطاء:

### المشكلة: Webhook لم يتم التعيين
```
الحل: تأكد من تعيين WEBHOOK_URL بشكل صحيح
```

### المشكلة: البوت لا يرد على الرسائل
```
الحل 1: تحقق من السجلات في Render
الحل 2: تأكد من أن WEBHOOK_SECRET صحيح
الحل 3: تأكد من البيانات الحساسة
```

### المشكلة: خطأ في CORS
```
الحل: Flask-CORS مثبت بالفعل
```

---

## 📞 الدعم:

```
Telegram: @Zi_ad_02
WhatsApp: +20 112 030 0273
Email: support@7ayahonline.com
```

---

## ✅ قائمة التحقق:

- [ ] تثبيت Flask و gunicorn
- [ ] تحديث requirements.txt
- [ ] إنشاء bot_webhook.py
- [ ] اختبار محلي
- [ ] إنشاء حساب Render
- [ ] رفع على GitHub
- [ ] ربط مع Render
- [ ] تعيين WEBHOOK_URL
- [ ] تعيين WEBHOOK_SECRET
- [ ] النشر والاختبار

---

## 🎉 بعد النشر:

```
✅ البوت يعمل 24/7
✅ حتى لو أطفأت اللابتوب
✅ استجابة فورية
✅ استهلاك موارد قليل
✅ لا توقف للخدمة ✨
```

---

**مبروك! البوت جاهز للعمل الدائم! 🚀**
