# 🚀 دليل النشر على Render

## 📋 المتطلبات

- ✅ حساب GitHub (يحتوي على المشروع)
- ✅ حساب Render (مجاني على https://render.com)
- ✅ رابط المستودع على GitHub

---

## 🔗 الروابط المهمة

| الخدمة | الرابط |
|--------|--------|
| **GitHub** | https://github.com/7ayahonline/Worm-GPT.git |
| **Render Dashboard** | https://dashboard.render.com |
| **Render Docs** | https://render.com/docs |

---

## 📝 خطوات النشر على Render

### 1️⃣ **إنشاء حساب Render** (إذا لم يكن لديك)

1. اذهب إلى: https://render.com
2. اضغط **Sign up**
3. اختر **Sign up with GitHub** (الأسهل)
4. وافق على الأذونات
5. تم! لديك حساب الآن

---

### 2️⃣ **إنشاء Web Service جديد**

1. ادخل إلى: https://dashboard.render.com
2. اضغط **+ New +**
3. اختر **Web Service**

---

### 3️⃣ **ربط مستودع GitHub**

1. في صفحة إنشاء الخدمة:
   - اختر **GitHub** من التوصيلات
   - اختر **Worm-GPT** من القائمة
   
2. إذا لم تظهر قائمة المستودعات:
   - اضغط **Connect account**
   - صرّح Render بالوصول إلى GitHub
   - أعد المحاولة

---

### 4️⃣ **إعدادات الخدمة**

#### **الإعدادات الأساسية:**

| الحقل | القيمة |
|------|--------|
| **Name** | `worm-gpt-bot` |
| **Environment** | `Python 3` |
| **Region** | اختر الأقرب (مثلاً `Singapore`) |
| **Branch** | `master` |

#### **الأوامر:**

```bash
Build Command:  pip install -r requirements.txt
Start Command:  python bot.py
```

#### **البيانات الثابتة:**
- لا تحتاج إلى تعيينها هنا (ستضيفها لاحقاً)

---

### 5️⃣ **إضافة متغيرات البيئة**

بعد إنشاء الخدمة:

1. اذهب إلى **Environment** في الإعدادات
2. أضف كل متغير:

```
TELEGRAM_BOT_TOKEN = YOUR_BOT_TOKEN
TELEGRAM_BOT_ID = YOUR_BOT_ID
ADMIN_IDS = YOUR_ADMIN_ID
PAYPAL_CLIENT_ID = YOUR_PAYPAL_ID
PAYPAL_SECRET = YOUR_PAYPAL_SECRET
PAYPAL_ENV = sandbox (أو production)
PAYPAL_ME_LINK = https://www.paypal.me/yourname
```

3. اضغط **Save**

---

### 6️⃣ **النشر**

#### **الطريقة الأولى: النشر اليدوي**
1. اضغط **Deploy** من الصفحة الرئيسية
2. انتظر حتى ينتهي البناء

#### **الطريقة الثانية: النشر التلقائي**
1. في الإعدادات، فعّل **Auto-Deploy**
2. في كل push على GitHub، سيتم النشر تلقائياً

---

## 🔍 مراقبة النشر

### عرض حالة النشر:
```
Dashboard → worm-gpt-bot → Deploys
```

### عرض السجلات:
```
Dashboard → worm-gpt-bot → Logs
```

### إعادة النشر:
```
Dashboard → worm-gpt-bot → Deploy
```

---

## 🐛 استكشاف الأخطاء

### إذا فشل البناء:

1. **تحقق من السجلات:**
   - اذهب إلى **Logs**
   - ابحث عن كلمة **error**

2. **المشاكل الشائعة:**

   **مشكلة:** `ModuleNotFoundError: No module named 'requests'`
   ```
   الحل: تأكد من وجود requirements.txt صحيح
   ```

   **مشكلة:** `Port is not available`
   ```
   الحل: غيّر المنفذ في البوت إلى:
   import os
   PORT = os.environ.get('PORT', 8000)
   ```

   **مشكلة:** `TELEGRAM_BOT_TOKEN not found`
   ```
   الحل: أضف متغيرات البيئة في Environment
   ```

### إذا لم يشتغل البوت:

1. تحقق من **Logs**:
   ```
   Dashboard → worm-gpt-bot → Logs
   ```

2. تحقق من متغيرات البيئة:
   ```
   Dashboard → worm-gpt-bot → Environment
   ```

3. جرّب إعادة النشر:
   ```
   Dashboard → worm-gpt-bot → Manual Deploy
   ```

---

## ⚙️ إعدادات متقدمة

### تغيير حجم الخادم:

1. اذهب إلى **Plan**
2. اختر **Free** (مجاني) أو **Starter** (مدفوع)

### تعطيل Auto-Deploy:

1. اذهب إلى **Settings**
2. ابحث عن **Auto-Deploy**
3. اضغط **Disable**

### حذف الخدمة:

1. اذهب إلى **Settings**
2. اضغط **Delete Web Service**
3. اكتب اسم الخدمة للتأكيد

---

## 📊 الخطة المجانية

### الحدود:
- ✅ **1 ساعة من وقت التشغيل**: يتم إعادة تشغيل الخدمة كل 24 ساعة
- ✅ **1 GB من الذاكرة**
- ✅ **0.5 CPU**
- ❌ **لا يوجد Custom Domains**

### الترقية:
إذا احتجت خطة مدفوعة:
- **Starter**: $7/شهر
- **Standard**: $25/شهر
- **Professional**: $125+/شهر

---

## 🔗 الروابط النهائية

بعد النشر، ستحصل على:

```
🌐 رابط البوت (Render): https://worm-gpt-bot.onrender.com
📱 رابط GitHub: https://github.com/7ayahonline/Worm-GPT.git
💬 رابط Telegram: @Ts_6_Bot
```

---

## 📞 خطوات تفصيلية بالصور

### الخطوة 1: ادخل Render
```
https://dashboard.render.com
```

### الخطوة 2: إنشاء Web Service
```
+ New → Web Service
```

### الخطوة 3: اختر GitHub
```
Connect GitHub account → Select Worm-GPT
```

### الخطوة 4: الإعدادات
```
Name: worm-gpt-bot
Environment: Python 3
Branch: master
Build: pip install -r requirements.txt
Start: python bot.py
```

### الخطوة 5: متغيرات البيئة
```
Environment → Add from file (.env) أو يدويًا
```

### الخطوة 6: Deploy
```
Create Web Service → Deploy
```

---

## ✅ قائمة التحقق قبل النشر

- [ ] تحديث `requirements.txt` مع جميع المكتبات
- [ ] تأكد من وجود `Procfile` و `render.yaml`
- [ ] نسخ `.env.example` وتعديل البيانات
- [ ] رفع آخر نسخة على GitHub
- [ ] إنشاء حساب Render
- [ ] ربط حساب GitHub مع Render
- [ ] إضافة متغيرات البيئة
- [ ] اختبار النشر

---

## 🎯 بعد النشر بنجاح

1. **اختبر البوت:**
   - أرسل `/start` إلى @Ts_6_Bot
   - تحقق من الاستجابة

2. **راقب السجلات:**
   - اذهب إلى **Logs**
   - تأكد من عدم وجود أخطاء

3. **فعّل Auto-Deploy:**
   - في كل push على GitHub، سيتم التحديث تلقائياً

4. **أضف شارة النشر (Badge):**
   ```markdown
   [![Deployed on Render](https://img.shields.io/badge/deployed-on%20Render-46EA00?logo=render&logoColor=white)](https://render.com)
   ```

---

## 🔒 نصائح الأمان

1. **لا تضع `.env` على GitHub:**
   - استخدم `.env.example` فقط
   - أضف `.env` في `.gitignore`

2. **متغيرات البيئة الحساسة:**
   - أضفها في Render Dashboard
   - لا تكتبها في الكود

3. **تحديث المفاتيح:**
   - غيّر التوكنات بانتظام
   - عطّل المفاتيح القديمة

---

## 📈 مراقبة الأداء

في Dashboard:
```
Metrics → CPU Usage, Memory, Network
```

---

## 💰 التكاليف

| الخطة | السعر | الحد الأقصى |
|------|-------|-----------|
| **Free** | $0 | 1 ساعة/يوم |
| **Starter** | $7 | 750 ساعة/شهر |
| **Standard** | $25 | غير محدود |

---

## 🎓 موارد إضافية

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [GitHub Integration](https://render.com/docs/github)

---

**تم بنجاح! البوت نشر على Render! 🎉**

للمساعدة:
- 📞 support@7ayahonline.com
- 💬 @Zi_ad_02
- 📱 +20 112 030 0273
