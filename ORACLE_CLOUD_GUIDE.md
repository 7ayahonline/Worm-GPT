# 🔥 Oracle Cloud VPS - دليل الإعداد الكامل

## 📋 المحتويات
1. [إنشاء حساب Oracle Cloud](#1-إنشاء-حساب-oracle-cloud)
2. [إنشاء VPS Instance](#2-إنشاء-vps-instance)
3. [الاتصال بالسيرفر](#3-الاتصال-بالسيرفر)
4. [تثبيت البوت](#4-تثبيت-البوت)
5. [إعداد Firewall](#5-إعداد-firewall)
6. [المراقبة والصيانة](#6-المراقبة-والصيانة)

---

## 1️⃣ إنشاء حساب Oracle Cloud

### **الخطوة أ: التسجيل**

1. **افتح الرابط:**
   ```
   https://www.oracle.com/cloud/free/
   ```

2. **اضغط "Start for free"**

3. **املأ البيانات:**
   - ✅ **Account Type:** اختر "Company"
   - ✅ **Cloud Account Name:** اسم فريد (مثل: wormgpt-bot-2025)
   - ✅ **Home Region:** اختر أقرب منطقة (مثل: Germany Central Frankfurt)
   - ✅ **Email:** إيميلك
   - ✅ **Password:** كلمة مرور قوية

4. **تأكيد الإيميل:**
   - افتح إيميلك
   - اضغط على رابط التحقق

5. **إضافة بيانات الدفع (للتحقق فقط):**
   ⚠️ **مهم:** Oracle تطلب بطاقة فيزا/ماستر كارد للتحقق فقط
   - ❌ **لن يتم خصم أي رسوم**
   - ✅ **المطلوب:** بطاقة صالحة (حتى لو فيها 1$ فقط)
   - ✅ **البديل:** استخدم بطاقة افتراضية (مثل CIB Virtual Card)

6. **بعد الموافقة:**
   - ستصلك رسالة: "Your account is ready"
   - سجّل دخول على: https://cloud.oracle.com

---

## 2️⃣ إنشاء VPS Instance

### **الخطوة ب: إنشاء السيرفر المجاني**

1. **من الـ Dashboard، اضغط:**
   ```
   Create a VM instance
   ```
   أو
   ```
   Menu ☰ → Compute → Instances → Create Instance
   ```

2. **إعدادات Instance:**

   | الإعداد | القيمة الموصى بها |
   |---------|-------------------|
   | **Name** | `worm-gpt-bot` |
   | **Compartment** | (root) - الافتراضي |
   | **Placement** | (افتراضي) |
   | **Image** | **Canonical Ubuntu 22.04** |
   | **Shape** | **VM.Standard.E2.1.Micro** (Always Free) |
   | **Primary VNIC** | (افتراضي) |
   | **Add SSH keys** | ⚠️ مهم جداً! اقرأ بالأسفل |

3. **إعداد SSH Key (مهم!):**

   **الخيار أ: Generate SSH key pair (الأسهل)**
   ```
   1. اختر "Generate a key pair for me"
   2. اضغط "Save Private Key" ← احفظ الملف على جهازك
   3. اضغط "Save Public Key" ← احفظه كمان
   4. ⚠️ لا تفقد هذا الملف! (لن تستطيع الدخول بدونه)
   ```

   **الخيار ب: Upload public key**
   ```
   إذا كان عندك SSH key بالفعل، ارفع الـ public key
   ```

4. **اضغط "Create"**

5. **انتظر 1-2 دقيقة حتى يصبح:**
   ```
   Status: ● Running
   ```

6. **احفظ المعلومات:**
   - ✅ **Public IP Address:** (مثل: 158.179.12.34)
   - ✅ **Username:** `ubuntu`
   - ✅ **Private Key:** (الملف اللي حملته)

---

## 3️⃣ الاتصال بالسيرفر

### **على Windows:**

#### **الطريقة 1: استخدام PuTTY (سهلة)**

1. **نزّل PuTTY:**
   ```
   https://www.putty.org/
   ```

2. **حوّل Private Key إلى صيغة PPK:**
   ```
   1. افتح "PuTTYgen"
   2. اضغط "Load"
   3. اختر الـ Private Key اللي حملته
   4. اضغط "Save private key"
   5. احفظه باسم: oracle-key.ppk
   ```

3. **افتح PuTTY:**
   ```
   Host Name: ubuntu@YOUR_PUBLIC_IP
   Port: 22
   Connection type: SSH
   
   في القائمة الجانبية:
   Connection → SSH → Auth → Credentials
   Private key file: اختر oracle-key.ppk
   
   اضغط Open
   ```

4. **أول مرة ستظهر رسالة تحذير → اضغط "Accept"**

5. **ستدخل على السيرفر مباشرة!**

---

#### **الطريقة 2: استخدام PowerShell (أسرع)**

1. **افتح PowerShell**

2. **انسخ الـ Private Key للمجلد الصحيح:**
   ```powershell
   mkdir $HOME\.ssh -Force
   copy "C:\Downloads\ssh-key-*.key" $HOME\.ssh\oracle-key
   ```

3. **اضبط صلاحيات الملف:**
   ```powershell
   icacls "$HOME\.ssh\oracle-key" /inheritance:r
   icacls "$HOME\.ssh\oracle-key" /grant:r "$($env:USERNAME):(R)"
   ```

4. **اتصل بالسيرفر:**
   ```powershell
   ssh -i $HOME\.ssh\oracle-key ubuntu@YOUR_PUBLIC_IP
   ```

   **استبدل `YOUR_PUBLIC_IP` بالـ IP الفعلي!**

---

### **على Linux/Mac:**

```bash
# نقل الـ Private Key
mv ~/Downloads/ssh-key-*.key ~/.ssh/oracle-key

# ضبط الصلاحيات
chmod 600 ~/.ssh/oracle-key

# الاتصال
ssh -i ~/.ssh/oracle-key ubuntu@YOUR_PUBLIC_IP
```

---

## 4️⃣ تثبيت البوت

### **الطريقة السريعة (أوتوماتيكية):**

بعد الاتصال بالسيرفر، نفّذ الأمر ده:

```bash
curl -sL https://raw.githubusercontent.com/7ayahonline/Worm-GPT/master/oracle_setup.sh | bash
```

**✅ هذا الأمر سيقوم بـ:**
- تحديث النظام
- تثبيت Python والمكتبات
- تنزيل البوت من GitHub
- إنشاء ملف .env
- إنشاء خدمة systemd
- تشغيل البوت تلقائياً
- فتح البورت المطلوب

**⏱️ الوقت المتوقع: 3-5 دقائق**

---

### **الطريقة اليدوية (خطوة بخطوة):**

إذا كنت تريد التحكم الكامل:

```bash
# 1. تحديث النظام
sudo apt update && sudo apt upgrade -y

# 2. تثبيت المكتبات
sudo apt install -y python3 python3-pip python3-venv git curl

# 3. استنساخ المشروع
git clone https://github.com/7ayahonline/Worm-GPT.git
cd Worm-GPT

# 4. إنشاء بيئة افتراضية
python3 -m venv venv
source venv/bin/activate

# 5. تثبيت المتطلبات
pip install -r requirements.txt

# 6. إنشاء ملف .env
nano .env
```

**محتوى ملف .env:**
```env
TELEGRAM_BOT_TOKEN=8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk
WEBHOOK_URL=http://YOUR_PUBLIC_IP:5000/webhook
WEBHOOK_SECRET=worm-gpt-secret-2025-secure
PORT=5000
ENVIRONMENT=production
```

**احفظ بـ: Ctrl+O ثم Enter ثم Ctrl+X**

```bash
# 7. اختبار البوت (اختياري)
python bot_webhook.py

# إذا اشتغل → اضغط Ctrl+C لإيقافه
```

---

## 5️⃣ إعداد Firewall

### **أ) Oracle Cloud Firewall (إجباري!):**

**⚠️ Oracle Cloud بتسد جميع البورتات افتراضياً!**

1. **ارجع لـ Oracle Cloud Dashboard**

2. **اذهب إلى:**
   ```
   Menu ☰ → Networking → Virtual Cloud Networks
   ```

3. **اضغط على الـ VCN الخاص بالـ Instance**

4. **اضغط على "Security Lists" → "Default Security List"**

5. **اضغط "Add Ingress Rules"**

6. **أضف القاعدة التالية:**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Source Port Range: (leave blank)
   Destination Port Range: 5000
   Description: Telegram Webhook
   ```

7. **اضغط "Add Ingress Rules"**

---

### **ب) Ubuntu Firewall (اختياري):**

```bash
# فتح البورت 5000
sudo ufw allow 5000/tcp

# تفعيل الـ Firewall
sudo ufw enable

# التحقق
sudo ufw status
```

---

## 6️⃣ المراقبة والصيانة

### **أوامر أساسية:**

```bash
# 🔍 مراقبة حالة البوت
sudo systemctl status worm-gpt-bot

# 📋 عرض آخر 50 سطر من اللوجات
sudo journalctl -u worm-gpt-bot -n 50

# 📜 متابعة اللوجات الحية (Real-time)
sudo journalctl -u worm-gpt-bot -f

# 🔄 إعادة تشغيل البوت
sudo systemctl restart worm-gpt-bot

# 🛑 إيقاف البوت
sudo systemctl stop worm-gpt-bot

# ▶️ تشغيل البوت
sudo systemctl start worm-gpt-bot

# 📊 عرض استخدام الموارد
htop
# (اضغط q للخروج)
```

---

### **تحديث البوت:**

```bash
cd ~/Worm-GPT
git pull origin master
sudo systemctl restart worm-gpt-bot
```

---

### **اختبار الـ Webhook:**

```bash
# من السيرفر نفسه
curl http://localhost:5000/health

# يجب أن يرد:
# {"status": "healthy", "timestamp": "..."}
```

```bash
# من جهازك (في PowerShell أو Terminal)
curl http://YOUR_PUBLIC_IP:5000/health
```

---

## 🐛 حل المشاكل الشائعة

### **❌ البوت لا يرد على Telegram:**

**1. تحقق من اللوجات:**
```bash
sudo journalctl -u worm-gpt-bot -n 100
```

**2. تحقق من الـ Webhook URL:**
```bash
# يجب أن يكون صحيح في ملف .env
cat ~/Worm-GPT/.env | grep WEBHOOK_URL
```

**3. اختبر الاتصال:**
```bash
curl http://YOUR_PUBLIC_IP:5000/
# يجب أن يرد: {"status": "running", "bot": "Worm GPT Bot", ...}
```

**4. تحقق من Oracle Cloud Firewall:**
- راجع الخطوة 5 أعلاه
- تأكد من إضافة Ingress Rule للبورت 5000

---

### **❌ "ModuleNotFoundError: No module named 'flask'":**

```bash
cd ~/Worm-GPT
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart worm-gpt-bot
```

---

### **❌ "Address already in use" أو "Port 5000 is already in use":**

```bash
# ابحث عن العملية المستخدمة للبورت
sudo lsof -i :5000

# أوقف العملية
sudo kill -9 <PID>

# أو أعد تشغيل السيرفر
sudo reboot
```

---

### **❌ فقدت SSH Private Key:**

⚠️ **لا يوجد حل مباشر!**

الحلول:
1. إذا كان البوت شغال → اتركه كما هو
2. أنشئ Instance جديد مع SSH key جديد
3. استخدم Oracle Cloud Console للوصول (Serial Console)

---

## 📊 مقارنة الحلول

| الميزة | Oracle Cloud VPS | Google Colab | Render |
|--------|-----------------|--------------|--------|
| **السعر** | 🟢 مجاني للأبد | 🟢 مجاني | 🟡 مجاني (Sleep) |
| **التشغيل 24/7** | 🟢 دائماً | 🟡 12 ساعة | 🟢 دائماً |
| **الأداء** | 🟢 ممتاز | 🟡 جيد | 🟢 ممتاز |
| **الاستقرار** | 🟢 عالي جداً | 🔴 متوسط | 🟢 عالي |
| **سهولة الإعداد** | 🟡 متوسط (10 دقائق) | 🟢 سهل (5 دقائق) | 🟢 سهل (7 دقائق) |
| **التحكم** | 🟢 كامل | 🔴 محدود | 🟡 متوسط |
| **Static IP** | 🟢 نعم | 🔴 لا | 🟢 نعم |

---

## ✅ الخلاصة

### **Oracle Cloud VPS هو الأفضل إذا:**
- ✅ تريد تشغيل دائم 24/7 بدون انقطاع
- ✅ تحتاج تحكم كامل في السيرفر
- ✅ تريد استخدام مجاني مدى الحياة
- ✅ تريد IP ثابت
- ✅ تريد تشغيل أكثر من بوت على نفس السيرفر

### **استخدم Colab إذا:**
- ✅ تريد إعداد سريع جداً (5 دقائق)
- ✅ لا تمانع إعادة التشغيل كل 12 ساعة
- ✅ لا تريد التعامل مع سيرفرات

### **استخدم Render إذا:**
- ✅ تريد إعداد سهل مع تشغيل دائم
- ✅ لا تمانع الـ Cold Start (15 دقيقة sleep)
- ✅ تريد CI/CD تلقائي من GitHub

---

## 📞 الدعم

**إذا واجهت أي مشكلة:**
- **Telegram:** @Zi_ad_02
- **WhatsApp:** +20 112 030 0273
- **GitHub Issues:** https://github.com/7ayahonline/Worm-GPT/issues

---

## 🎉 النتيجة النهائية

```
✅ VPS مجاني مدى الحياة
✅ البوت شغال 24/7 بدون توقف
✅ لا حاجة لترك اللابتوب
✅ IP ثابت
✅ أداء عالي
✅ تحكم كامل
```

**🚀 ابدأ الآن!**
