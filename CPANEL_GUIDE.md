# 🌐 تفاصيل الوصول إلى cPanel - 7ayahonline

## 📋 معلومات الاستضافة

| المعلومة | التفاصيل |
|---------|---------|
| **موقع الاستضافة** | 7ayahonline.com |
| **نوع الاستضافة** | Shared Hosting / cPanel |
| **الدعم** | Support@7ayahonline.com |

---

## 🔐 روابط الوصول

### 1️⃣ **رابط cPanel الرئيسي:**
```
https://cpanel.7ayahonline.com/
أو
https://7ayahonline.com:2083/
```

### 2️⃣ **رابط Webmail:**
```
https://webmail.7ayahonline.com/
أو
https://mail.7ayahonline.com/
```

### 3️⃣ **رابط File Manager (مباشر):**
```
https://cpanel.7ayahonline.com/cpsess_xxxx/frontend/x3/filemanager/index.html
(يتم التوليد بعد تسجيل الدخول)
```

---

## 👤 بيانات تسجيل الدخول

### cPanel Login:
```
Username (المستخدم):    [أدخل اسم المستخدم]
Password (كلمة المرور):  [أدخل كلمة المرور]
```

### FTP Details:
```
Server (الخادم):         ftp.7ayahonline.com
Username (المستخدم):    [اسم مستخدم FTP - عادة نفس cPanel]
Password (كلمة المرور):  [كلمة مرور FTP]
Port (المنفذ):          21
Passive Mode:           ✅ تفعيل
```

### SSH Access:
```
Server (الخادم):         7ayahonline.com
Username (المستخدم):    [اسم المستخدم]
Password (كلمة المرور):  [كلمة المرور]
Port (المنفذ):          22
```

---

## 🗂️ هيكل الملفات في cPanel

```
/public_html/                    ← المجلد الرئيسي للموقع
├── bot.py                        ← البوت الرئيسي
├── bot_stats.json               ← إحصائيات البوت
├── users_data.json              ← بيانات المستخدمين
├── admin_actions.json           ← سجل الإجراءات
├── coupons.json                 ← الكوبونات
├── .env                         ← متغيرات البيئة (سرية)
├── .htaccess                    ← إعدادات الأمان
├── requirements.txt             ← المتطلبات
├── run.sh                       ← سكريبت التشغيل (Linux)
└── /docs/                       ← الملفات الموثقة
    ├── README.md
    ├── CONFIGURATION.md
    └── DEPLOY.md
```

---

## 📝 خطوات الوصول للمرة الأولى

### عبر المتصفح:

1. **اذهب إلى:** `https://cpanel.7ayahonline.com/`
2. **أدخل:**
   - Username (اسم المستخدم)
   - Password (كلمة المرور)
3. **اضغط:** Sign In

### عبر FTP (باستخدام FileZilla):

1. **حمّل FileZilla** من: https://filezilla-project.org/
2. **أدخل البيانات:**
   - Host: `ftp://ftp.7ayahonline.com`
   - Username: `[اسم المستخدم FTP]`
   - Password: `[كلمة المرور]`
   - Port: `21`
3. **اضغط:** Quickconnect

### عبر SSH (باستخدام Terminal/Putty):

```bash
ssh username@7ayahonline.com
# أدخل كلمة المرور
# تم الاتصال!
```

---

## 🚀 خطوات رفع البوت

### الطريقة 1️⃣: عبر File Manager (من cPanel)

1. ادخل cPanel
2. اذهب إلى **File Manager**
3. انقر على مجلد **public_html**
4. اضغط **Upload**
5. اختر الملفات:
   - `bot.py`
   - `requirements.txt`
   - `bot_stats.json`
   - `users_data.json`
   - `coupons.json`
   - `admin_actions.json`
   - `.env` (ملف حساس - نسخه يدويًا)

### الطريقة 2️⃣: عبر FTP (أسرع للملفات الكبيرة)

1. افتح FileZilla
2. اتصل بـ FTP
3. اسحب الملفات من جهازك المحلي إلى `/public_html/`

### الطريقة 3️⃣: عبر SSH + Git (الأفضل)

```bash
# اتصل بـ SSH
ssh username@7ayahonline.com

# انتقل للمجلد
cd public_html

# انسخ المشروع
git clone https://github.com/YOUR_USERNAME/worm-gpt-bot.git

# ادخل المجلد
cd worm-gpt-bot

# ثبت المتطلبات
pip install -r requirements.txt

# شغل البوت
python bot.py
```

---

## 🔧 الأدوات المتاحة في cPanel

### 1️⃣ **File Manager** - إدارة الملفات
```
Files → File Manager
```

### 2️⃣ **Terminal** - سطر الأوامر (إذا كان متاحاً)
```
Advanced → Terminal
```

### 3️⃣ **Cron Jobs** - جدولة المهام
```
Advanced → Cron Jobs
(لجدولة تشغيل البوت تلقائيًا)
```

### 4️⃣ **MySQL Databases** - قواعد البيانات
```
Databases → MySQL® Databases
(إذا احتجت database في المستقبل)
```

### 5️⃣ **Email Accounts** - البريد الإلكتروني
```
Email → Email Accounts
```

---

## ⚙️ الإعدادات المهمة

### تشغيل البوت تلقائياً:

في cPanel:
1. اذهب إلى **Cron Jobs**
2. أضف:
```bash
@reboot cd /home/username/public_html && python bot.py > bot.log 2>&1 &
```

أو للتشغيل كل ساعة:
```bash
0 * * * * /usr/bin/python3 /home/username/public_html/bot.py
```

### حماية الملفات الحساسة:

في `.htaccess`:
```apache
<Files ".env">
    Order allow,deny
    Deny from all
</Files>

<Files "*.json">
    Order allow,deny
    Deny from all
</Files>
```

---

## 📊 فحص الموارد

في cPanel:
1. اذهب إلى **Resource Usage**
2. شاهد:
   - استهلاك CPU
   - استهلاك الذاكرة
   - عدد العمليات

---

## 🐛 استكشاف الأخطاء

### إذا كان هناك خطأ:

1. **شاهد السجلات:**
```bash
ssh username@7ayahonline.com
cd public_html
tail -f bot.log
```

2. **تحقق من Python:**
```bash
python --version
pip --version
```

3. **تحقق من الملفات:**
```bash
ls -la
cat .env
```

### إذا لم يشتغل البوت:

1. تأكد من وجود `requirements.txt` و `bot.py`
2. ثبت المتطلبات: `pip install -r requirements.txt`
3. شاهد الأخطاء: `python bot.py`

---

## 🔗 روابط مهمة سريعة

| الخدمة | الرابط |
|--------|---------|
| cPanel | https://cpanel.7ayahonline.com |
| Webmail | https://webmail.7ayahonline.com |
| FTP | ftp://ftp.7ayahonline.com |
| الدعم | support@7ayahonline.com |
| الموقع | https://7ayahonline.com |

---

## 📞 معلومات الدعم الفني

| القناة | التفاصيل |
|--------|----------|
| **البريد الإلكتروني** | support@7ayahonline.com |
| **الهاتف** | (عادة موجود في الفاتورة) |
| **الدردشة** | (من موقع الاستضافة) |
| **لوحة التحكم** | cpanel.7ayahonline.com |

---

## 🎯 ملخص سريع

✅ ادخل cPanel: `cpanel.7ayahonline.com`
✅ اذهب إلى File Manager
✅ ارفع `bot.py` و الملفات الأخرى
✅ شغل: `python bot.py`
✅ شاهد السجلات في Terminal

---

**هل تحتاج مساعدة في أي خطوة معينة؟** 📞
