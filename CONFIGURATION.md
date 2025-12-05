# ⚙️ إعدادات وتكوين Worm GPT Bot

## 📋 متطلبات النظام

- Python 3.8+
- مكتبة `requests`
- حساب Telegram Bot (من @BotFather)
- ملفات JSON للبيانات (يتم إنشاؤها تلقائياً)

---

## 🔑 المتغيرات الأساسية

### في `bot.py`:

```python
BOT_TOKEN = "YOUR_TOKEN_HERE"  # من @BotFather
DEVELOPER_ID = YOUR_DEVELOPER_ID  # رقم آيديك (مثال: 8416721882)
ADMIN_IDS = [YOUR_DEVELOPER_ID]  # قائمة رقام المديرين
API_URL = "https://worm-gpt.faresveno.workers.dev/"  # API الذكاء الاصطناعي
```

### متغيرات PayPal (متغيرات البيئة):

```bash
# في Windows:
set PAYPAL_CLIENT_ID=your_client_id
set PAYPAL_SECRET=your_secret
set PAYPAL_ENV=sandbox  # أو live للإنتاج
set PAYPAL_ME_LINK=https://paypal.me/yourlink
```

```bash
# في Linux/Mac:
export PAYPAL_CLIENT_ID=your_client_id
export PAYPAL_SECRET=your_secret
export PAYPAL_ENV=sandbox
export PAYPAL_ME_LINK=https://paypal.me/yourlink
```

---

## 💰 تكوين الباقات

في `bot.py`، يمكن تعديل الأسعار والمدد:

```python
PLANS = {
    "monthly_eg": {
        "name": "شهري عادي - مصر",
        "price": 299,  # المبلغ
        "currency": "EGP",  # العملة
        "days": 30,  # عدد الأيام
        "type": "عادي"  # نوع الباقة
    },
    "vip_monthly_eg": {
        "name": "شهري VIP - مصر",
        "price": 499,
        "currency": "EGP",
        "days": 30,
        "type": "VIP"
    },
    # ... الباقات الأخرى
}
```

---

## 📁 ملفات البيانات

### 1. `users_data.json`
يحفظ بيانات المستخدمين:
```json
{
  "8416721882": {
    "username": "username",
    "first_name": "Ahmed",
    "joined_date": "2025-12-05 13:00:00",
    "questions_count": 5,
    "subscription": {
      "active": true,
      "plan_code": "monthly_eg",
      "expires_at": "2025-12-05 14:00:00",
      "free_remaining": 0
    }
  }
}
```

### 2. `bot_stats.json`
إحصائيات البوت:
```json
{
  "total_users": 10,
  "total_questions": 100,
  "successful_responses": 95,
  "failed_responses": 5,
  "last_week_report_week": "2025-W49"
}
```

### 3. `coupons.json`
الكوبونات:
```json
[
  {
    "code": "WELCOME50",
    "plan": "any",
    "discountType": "percent",
    "discountValue": 50,
    "maxUses": 10,
    "usedCount": 3,
    "expiresAt": "2025-12-31 23:59:59",
    "active": true,
    "notes": "كوبون الترحيب"
  }
]
```

### 4. `admin_actions.json`
سجل الإجراءات الإدارية:
```json
[
  {
    "time": "2025-12-05 13:00:00",
    "actor": 8416721882,
    "action": "activate",
    "details": "تفعيل monthly_eg للمستخدم 1234567890"
  }
]
```

---

## 🚀 التشغيل

### الطريقة 1: مباشر
```bash
python bot.py
```

### الطريقة 2: عبر run.bat (Windows)
```bash
run.bat
```

### الطريقة 3: في الخلفية (Linux/Mac)
```bash
nohup python bot.py > bot.log 2>&1 &
```

---

## 🔄 إعادة التشغيل الآمنة

البوت يستخدم:
- **ملف الـ lock:** `bot.lock` - لمنع نسخ متعددة
- **حذف Webhook:** تلقائياً عند البدء
- **auto-restart:** في `run.bat` عند أي خطأ

---

## 📊 الأوامر الإدارية

### للمطورين:
```
/admin - لوحة الإدارة
/activate <user_id> <plan_code> - تفعيل اشتراك
/revoke <user_id> - إلغاء اشتراك
/extend <user_id> <days> - تمديد اشتراك
/broadcast <message> - إرسال رسالة لكل المستخدمين
/users - قائمة المستخدمين
```

### للكوبونات:
```
/coupon_create CODE PLAN TYPE VALUE MAXUSES EXPIRESDAYS [NOTES]
/coupon_enable CODE
/coupon_disable CODE
/coupon_list
/coupon_info CODE
```

**أنواع الكوبونات:**
- `percent` - نسبة مئوية
- `amount` - مبلغ ثابت
- `extend_days` - تمديد الاشتراك بأيام
- `extra_free` - أسئلة مجانية إضافية

---

## 🔒 الأمان

### نقاط الأمان المطبقة:

1. **متغيرات البيئة:** لا تخزين التوكنات في الكود
2. **Webhook الحذف:** منع التعارض مع webhook آخر
3. **Lock File:** منع نسخ متعددة من العمل
4. **أمان الكوبونات:** التحقق من التفعيل والصلاحية
5. **معالجة الأخطاء:** محاولات آمنة مع رسائل واضحة

---

## 🐛 استكشاف الأخطاء

### المشكلة: "Bot already running"
**الحل:** احذف `bot.lock` ثم شغّل البوت

### المشكلة: "409 Conflict"
**الحل:** البوت يحذف الـ webhook تلقائياً، حاول مرة أخرى

### المشكلة: "No module named requests"
**الحل:** 
```bash
pip install requests
```

### المشكلة: PayPal لا يعمل
**تأكد من:**
- متغيرات البيئة معرّفة صحيحة
- `PAYPAL_ENV` معرف (sandbox أو live)
- التوكنات صحيحة

---

## 📈 النسخ الاحتياطية

يفضل عمل نسخ احتياطية من:
```
- users_data.json
- bot_stats.json
- admin_actions.json
- coupons.json
```

---

## 🔄 التحديثات

للحصول على آخر تحديثات، شاهد:
- `CHANGELOG.md` - سجل التغييرات
- `AUDIT_REPORT.md` - تقرير الفحص

---

**آخر تحديث:** 5 ديسمبر 2025
