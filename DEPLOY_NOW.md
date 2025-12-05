# 🚀 نشر سريع على Render - 3 خطوات فقط!

## ⚡ **طريقة النشر الأسرع (دقيقتين)**

### **1️⃣ افتح Render Dashboard:**
🔗 [اضغط هنا للدخول](https://dashboard.render.com)

إذا لم يكن لديك حساب: اضغط "Sign up with GitHub"

---

### **2️⃣ أنشئ Web Service جديد:**

1. اضغط على **"+ New"** (أعلى اليمين)
2. اختر **"Web Service"**
3. اختر **"Connect account"** → GitHub
4. ابحث عن: **Worm-GPT**
5. اضغط **"Connect"**

---

### **3️⃣ املأ الإعدادات:**

```
Name:                worm-gpt-bot
Environment:         Python 3
Region:              Singapore (أو أي منطقة قريبة)
Branch:              master
Build Command:       pip install -r requirements.txt
Start Command:       python bot_webhook.py
```

---

### **4️⃣ أضف متغيرات البيئة:**

اضغط **"Environment"** → **"Add Environment Variable"**

أضف هذه المتغيرات:

```
TELEGRAM_BOT_TOKEN
القيمة: 8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk

WEBHOOK_SECRET
القيمة: worm-gpt-secret-2025-secure

ENVIRONMENT
القيمة: production
```

---

### **5️⃣ انشر!**

1. اضغط **"Create Web Service"**
2. انتظر 3-5 دقائق (النشر التلقائي)
3. عند الإكمال، ستحصل على رابط مثل:
   ```
   https://worm-gpt-bot.onrender.com
   ```

---

### **6️⃣ تحديث WEBHOOK_URL:**

بعد النشر الناجح:

1. انسخ رابط الخدمة (مثل: `https://worm-gpt-bot.onrender.com`)
2. اذهب إلى **Environment**
3. أضف متغير جديد:
   ```
   WEBHOOK_URL
   القيمة: https://worm-gpt-bot.onrender.com/webhook
   ```
4. اضغط **"Save Changes"**
5. الخدمة ستعيد النشر تلقائياً

---

### **7️⃣ اختبر البوت:**

1. افتح Telegram
2. ابحث عن: `@Ts_6_Bot`
3. أرسل: `/start`
4. يجب أن يرد فوراً! ✅

---

## 🎊 **مبروك! البوت يعمل الآن 24/7!**

```
✅ يعمل على السحابة
✅ حتى لو أطفأت اللابتوب
✅ استجابة فورية
✅ موثوق وآمن
```

---

## 📊 **مراقبة البوت:**

في Render Dashboard:
- **Logs**: شاهد سجلات البوت الحية
- **Metrics**: استهلاك الموارد
- **Events**: تاريخ النشر

---

## 🔧 **إذا واجهت مشاكل:**

### المشكلة: البوت لا يرد
```
الحل:
1. تحقق من Logs في Render
2. تأكد من TELEGRAM_BOT_TOKEN صحيح
3. تأكد من WEBHOOK_URL محدث
```

### المشكلة: خطأ في البناء
```
الحل:
1. تحقق من requirements.txt موجود
2. تأكد من bot_webhook.py موجود
3. جرب Manual Deploy
```

---

## 📞 **الدعم:**

```
Telegram: @Zi_ad_02
WhatsApp: +20 112 030 0273
GitHub: https://github.com/7ayahonline/Worm-GPT
```

---

## 🎯 **الخطة المجانية:**

```
✅ 750 ساعة/شهر (كافية للبوت)
✅ SSL مجاني
✅ Auto-deploy من GitHub
⚠️ النوم بعد 15 دقيقة من عدم النشاط
```

للعمل 24/7 بدون نوم: ترقى إلى **Starter** ($7/شهر)

---

**🚀 ابدأ الآن: https://dashboard.render.com**
