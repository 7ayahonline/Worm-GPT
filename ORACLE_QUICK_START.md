# ⚡ Oracle Cloud - تشغيل سريع (10 دقائق)

---

## 🎯 **3 خطوات فقط!**

### **1️⃣ أنشئ حساب Oracle Cloud (5 دقائق)**

```
1. افتح: https://www.oracle.com/cloud/free/
2. اضغط "Start for free"
3. املأ البيانات + بطاقة فيزا (للتحقق فقط - بدون خصم)
4. تأكيد الإيميل
5. سجل دخول: https://cloud.oracle.com
```

---

### **2️⃣ أنشئ VPS مجاني (3 دقائق)**

```
1. Dashboard → "Create a VM instance"

2. الإعدادات:
   Name: worm-gpt-bot
   Image: Ubuntu 22.04
   Shape: VM.Standard.E2.1.Micro (Always Free) ✅
   
3. SSH Key:
   - اختر "Generate a key pair for me"
   - احفظ Private Key (مهم جداً!)
   
4. اضغط "Create"

5. انتظر حتى Status: ● Running

6. احفظ Public IP (مثل: 158.179.12.34)
```

---

### **3️⃣ شغّل البوت (2 دقيقة)**

#### **أ) اتصل بالسيرفر:**

**على Windows (PuTTY):**
```
1. نزّل PuTTY: https://www.putty.org/
2. افتح PuTTYgen → Load → اختر Private Key → Save private key
3. افتح PuTTY:
   Host: ubuntu@YOUR_IP
   Auth → Private key: اختر الملف
4. اضغط Open
```

**على Windows (PowerShell) - أسهل:**
```powershell
ssh -i "C:\Downloads\ssh-key-*.key" ubuntu@YOUR_IP
```

---

#### **ب) ثبّت البوت (أمر واحد!):**

بعد الدخول للسيرفر، نفّذ:

```bash
curl -sL https://raw.githubusercontent.com/7ayahonline/Worm-GPT/master/oracle_setup.sh | bash
```

**⏱️ انتظر 3-5 دقائق...**

---

#### **ج) افتح البورت في Oracle Cloud:**

⚠️ **مهم جداً!**

```
1. ارجع لـ Oracle Dashboard
2. Menu ☰ → Networking → Virtual Cloud Networks
3. اضغط على VCN → Security Lists → Default
4. Add Ingress Rules:
   - Source CIDR: 0.0.0.0/0
   - Protocol: TCP
   - Port: 5000
5. Save
```

---

## ✅ **انتهى! البوت شغال!**

### **اختبر البوت:**
```
Telegram → @Ts_6_Bot → /start
```

---

## 📊 **أوامر مفيدة:**

```bash
# مراقبة البوت
sudo systemctl status worm-gpt-bot

# عرض اللوجات
sudo journalctl -u worm-gpt-bot -f

# إعادة تشغيل
sudo systemctl restart worm-gpt-bot

# تحديث البوت
cd ~/worm-gpt-bot
git pull
sudo systemctl restart worm-gpt-bot
```

---

## 🔥 **المميزات:**

```
✅ مجاني مدى الحياة
✅ شغال 24/7 بدون توقف
✅ IP ثابت
✅ أداء عالي
✅ لا حاجة للابتوب
```

---

## 📞 **الدعم:**
- Telegram: @Zi_ad_02
- WhatsApp: +20 112 030 0273

---

## 🚀 **ابدأ الآن!**

👉 https://www.oracle.com/cloud/free/
