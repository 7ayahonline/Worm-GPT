# 🚀 دليل تشغيل البوت على Google Colab

## 📌 لماذا Google Colab؟

✅ **مجاني 100%** - بدون أي تكاليف  
✅ **سهل جداً** - 6 خطوات فقط  
✅ **شغال 24/7** - مع Keep-Alive Trick  
✅ **بدون VPS** - لا حاجة لاستئجار سيرفر  
✅ **حفظ تلقائي** - كل البيانات محفوظة في Google Drive  

---

## 🎯 الخطوات (5 دقائق فقط!)

### **1️⃣ ارفع المشروع على Google Drive**

1. افتح [Google Drive](https://drive.google.com)
2. ارفع مجلد المشروع كامل (أو اسحبه وأفلته)
3. تأكد من وجود الملفات:
   - `bot_webhook.py`
   - `requirements.txt`
   - `users_data.json`
   - `bot_stats.json`
   - `coupons.json`

---

### **2️⃣ افتح Colab Notebook**

**اختر أحد الخيارات:**

#### **الخيار أ: من هذا المشروع**
1. افتح ملف `COLAB_SETUP.ipynb` من المشروع
2. اضغط عليه في Google Drive
3. اختر "Open with" → "Google Colaboratory"
4. ✅ كل الكود جاهز!

#### **الخيار ب: إنشاء Notebook جديد**
1. اذهب إلى: https://colab.research.google.com
2. اضغط "New Notebook"
3. انسخ الكود من `COLAB_SETUP.ipynb`

---

### **3️⃣ احصل على Ngrok Token**

Ngrok مطلوب لإنشاء URL عام للبوت (مجاني تماماً!)

1. **سجل حساب مجاني:**  
   👉 https://dashboard.ngrok.com/signup

2. **احصل على Authtoken:**  
   👉 https://dashboard.ngrok.com/get-started/your-authtoken

3. **انسخ Token** (شكله كده: `2abc...xyz`)

---

### **4️⃣ شغّل Notebook خطوة بخطوة**

افتح `COLAB_SETUP.ipynb` وشغّل الخلايا بالترتيب:

#### **الخلية 1: ربط Google Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
```
- ✅ هيطلب إذن → وافق
- ✅ هتشوف "Mounted at /content/drive"

---

#### **الخلية 2: تحديد مسار المشروع**
```python
PROJECT_PATH = "/content/drive/MyDrive/Worm-GPT"
os.chdir(PROJECT_PATH)
!ls -la
```
⚠️ **مهم:** غيّر `Worm-GPT` لاسم مجلدك في Drive

---

#### **الخلية 3: تثبيت المكتبات**
```python
!pip install -q -r requirements.txt
!pip install -q pyngrok
```
- ✅ هيثبت Flask, Gunicorn, pyngrok
- ✅ يأخذ 30-60 ثانية

---

#### **الخلية 4: تفعيل Ngrok**
```python
NGROK_TOKEN = "YOUR_NGROK_TOKEN_HERE"
ngrok.set_auth_token(NGROK_TOKEN)
```
⚠️ **استبدل** `YOUR_NGROK_TOKEN_HERE` بالـ Token اللي نسخته

---

#### **الخلية 5: تشغيل البوت 🚀**
```python
public_url = ngrok.connect(5000, bind_tls=True)
# ... بقية الكود ...
process = subprocess.Popen(['python', 'bot_webhook.py'])
```
- ✅ هيظهر Webhook URL
- ✅ البوت هيبدأ يشتغل فوراً
- ✅ اختبر على Telegram: `@Ts_6_Bot`

---

#### **الخلية 6: Keep-Alive (منع قطع الاتصال)**

**الطريقة الأولى (الأسهل):**
1. افتح Console في المتصفح: `Ctrl + Shift + I`
2. اذهب لتبويب **Console**
3. الصق الكود ده:

```javascript
function ClickConnect(){
  console.log("Clicking connect button...");
  document.querySelector("colab-toolbar-button#connect").click();
}
setInterval(ClickConnect, 60000);
console.log("Keep-Alive Started ✅");
```

**الطريقة الثانية:**
- شغّل الخلية 6 في Notebook مباشرة

---

### **5️⃣ راقب البوت**

#### **فحص الحالة (الخلية 7):**
```python
response = requests.get(f"{public_url}/health")
```
- ✅ هيقولك البوت شغال ولا لأ

#### **عرض الإحصائيات (الخلية 8):**
```python
with open('users_data.json', 'r') as f:
    users_data = json.load(f)
```
- ✅ عدد المستخدمين
- ✅ المشتركين النشطين
- ✅ إجمالي الأسئلة

---

### **6️⃣ إيقاف البوت (عند الحاجة)**

شغّل الخلية الأخيرة:
```python
process.terminate()
ngrok.kill()
```

---

## 🔥 نصائح مهمة

### ✅ **للتشغيل 24/7:**
1. **فعّل Keep-Alive** (الخطوة 4 - الخلية 6)
2. **اترك التبويب مفتوح** (يمكن تصغيره في الخلفية)
3. **استخدم GPU Runtime** (اختياري لأداء أفضل):
   - `Runtime` → `Change runtime type` → `GPU`

### ⚠️ **قيود Colab المجاني:**
- ✅ **12 ساعة** تشغيل متواصل (ثم يطلب إعادة تشغيل)
- ✅ **90 دقيقة** بعد آخر نشاط (Keep-Alive يحل المشكلة)
- ✅ **Ngrok URL يتغير** مع كل جلسة جديدة

### 💡 **حلول احترافية:**
- **للـ Static Domain:** ترقية Ngrok ($8/شهر)
- **للتشغيل الدائم:** Colab Pro ($10/شهر) أو Render (مجاني)
- **للأداء العالي:** Google Cloud Run أو AWS Lambda

---

## 📊 مقارنة الخيارات

| الميزة | Colab + Ngrok | Render | VPS |
|--------|--------------|--------|-----|
| **السعر** | 🟢 مجاني | 🟢 مجاني (Sleep) | 🔴 $5+/شهر |
| **السهولة** | 🟢 سهل جداً | 🟡 متوسط | 🔴 صعب |
| **التشغيل 24/7** | 🟡 12 ساعة | 🟢 دائماً | 🟢 دائماً |
| **الإعداد** | 🟢 5 دقائق | 🟡 10 دقائق | 🔴 30+ دقيقة |
| **الاستقرار** | 🟡 جيد | 🟢 ممتاز | 🟢 ممتاز |

---

## 🐛 حل المشاكل الشائعة

### **❌ "Mounted at /content/drive" لا يظهر**
**الحل:**
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

---

### **❌ "ModuleNotFoundError: No module named 'flask'"**
**الحل:**
```python
!pip install --upgrade flask flask-cors gunicorn requests
```

---

### **❌ "Invalid Ngrok Token"**
**الحل:**
1. تأكد من نسخ Token كامل (بدون مسافات)
2. احصل على Token جديد من: https://dashboard.ngrok.com/get-started/your-authtoken
3. تأكد من التسجيل في Ngrok أولاً

---

### **❌ "Webhook verification failed"**
**الحل:**
تأكد من:
```python
os.environ['WEBHOOK_SECRET'] = 'worm-gpt-secret-2025-secure'
```
يجب أن يطابق الـ Secret في `bot_webhook.py`

---

### **❌ البوت لا يرد على Telegram**
**الحل:**
1. **فحص Webhook URL:**
   ```python
   print(webhook_url)
   ```
   افتح الرابط في المتصفح → يجب أن يظهر `{"status": "running"}`

2. **فحص Logs:**
   ```python
   !tail -f /tmp/bot.log  # إذا كنت تكتب logs
   ```

3. **اختبار مباشر:**
   ```python
   import requests
   response = requests.get(f"{public_url}/health")
   print(response.json())
   ```

---

### **❌ "Colab disconnected"**
**الحل:**
- تأكد من تشغيل **Keep-Alive JavaScript** في Console
- اترك التبويب مفتوح (يمكن تصغيره)
- لا تغلق المتصفح تماماً

---

## 📁 هيكل الملفات المطلوب

```
Worm-GPT/               (مجلد على Google Drive)
├── bot_webhook.py      ✅ الملف الرئيسي
├── requirements.txt    ✅ المكتبات
├── users_data.json     ✅ بيانات المستخدمين
├── bot_stats.json      ✅ الإحصائيات
├── coupons.json        ✅ الكوبونات
└── COLAB_SETUP.ipynb   ✅ Notebook الإعداد
```

---

## 🎯 Quick Start (للمحترفين)

**خطوة واحدة فقط:**

1. افتح `COLAB_SETUP.ipynb` في Google Colab
2. غيّر في الخلية 2:
   ```python
   PROJECT_PATH = "/content/drive/MyDrive/YOUR_FOLDER_NAME"
   ```
3. غيّر في الخلية 4:
   ```python
   NGROK_TOKEN = "your_actual_ngrok_token"
   ```
4. شغّل **Runtime** → **Run all**
5. ✅ البوت شغال!

---

## 📞 الدعم والمساعدة

### **Telegram:**
- **@Zi_ad_02** ← مطور البوت

### **WhatsApp:**
- **+20 112 030 0273** ← دعم فني

### **GitHub:**
- **Repository:** https://github.com/7ayahonline/Worm-GPT
- **افتح Issue** للإبلاغ عن مشاكل

---

## 🎉 النتيجة النهائية

بعد اتباع الخطوات:

✅ البوت شغال على Google Colab  
✅ Webhook URL تلقائي من Ngrok  
✅ البيانات محفوظة في Google Drive  
✅ Keep-Alive يمنع قطع الاتصال  
✅ مراقبة سهلة للحالة والإحصائيات  
✅ **مجاني 100% بدون أي تكاليف!**  

---

## 🚀 **ابدأ الآن!**

1. **ارفع المشروع على Drive**
2. **افتح `COLAB_SETUP.ipynb`**
3. **احصل على Ngrok Token**
4. **شغّل الخلايا بالترتيب**
5. **فعّل Keep-Alive**
6. **اختبر البوت على Telegram**

**🎊 بالتوفيق! البوت دلوقتي شغال 24/7 مجاناً!**
