import logging
import requests
import json
from datetime import datetime, timedelta
import os
import threading
from typing import Dict, Any
from flask import Flask, request

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إنشاء تطبيق Flask
app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk")
DEVELOPER_ID = 8416721882
ADMIN_IDS = [8416721882]
API_URL = "https://worm-gpt.faresveno.workers.dev/"
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"
BOT_VERSION = "3.0.1"

# Webhook URL (سيتم تعيينها من متغيرات البيئة)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "worm-gpt-secret-key")

# إعدادات بايبال
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")
PAYPAL_ENV = os.getenv("PAYPAL_ENV", "sandbox")
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com" if PAYPAL_ENV == "sandbox" else "https://api-m.paypal.com"
PAYPAL_RECEIVE_LINK = os.getenv("PAYPAL_ME_LINK", "https://paypal.me/yourlink")

# الباقات والأسعار
PLANS = {
    "monthly_eg": {"name": "شهري عادي - مصر", "price": 299, "currency": "EGP", "days": 30, "type": "عادي"},
    "monthly_int": {"name": "شهري عادي - دولي", "price": 10, "currency": "USD", "days": 30, "type": "عادي"},
    "vip_monthly_eg": {"name": "شهري VIP - مصر", "price": 499, "currency": "EGP", "days": 30, "type": "VIP"},
    "vip_monthly_int": {"name": "شهري VIP - دولي", "price": 20, "currency": "USD", "days": 30, "type": "VIP"},
    "yearly_eg": {"name": "سنوي عادي - مصر", "price": 3228, "original": 3588, "currency": "EGP", "days": 365, "type": "عادي", "discount": "10%"},
    "yearly_int": {"name": "سنوي عادي - دولي", "price": 108, "original": 120, "currency": "USD", "days": 365, "type": "عادي", "discount": "10%"},
    "vip_yearly_eg": {"name": "سنوي VIP - مصر", "price": 5091, "original": 5988, "currency": "EGP", "days": 365, "type": "VIP", "discount": "15%"},
    "vip_yearly_int": {"name": "سنوي VIP - دولي", "price": 204, "original": 240, "currency": "USD", "days": 365, "type": "VIP", "discount": "15%"}
}

FREE_QUESTION_LIMIT = 5

# ملفات البيانات
STATS_FILE = "bot_stats.json"
USERS_FILE = "users_data.json"
ADMIN_LOG_FILE = "admin_actions.json"
COUPONS_FILE = "coupons.json"

# ================== دوال تحميل البيانات ==================

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data.setdefault("last_week_report_week", None)
            return data
    return {
        "total_users": 0,
        "total_questions": 0,
        "successful_responses": 0,
        "failed_responses": 0,
        "last_week_report_week": None
    }

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_coupons():
    if os.path.exists(COUPONS_FILE):
        try:
            with open(COUPONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def load_admin_log():
    if os.path.exists(ADMIN_LOG_FILE):
        try:
            with open(ADMIN_LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_admin_log(log):
    with open(ADMIN_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

stats = load_stats()
users_data = load_users()

# ================== دوال الـ Telegram API ==================

def tg_request(method: str, params: Dict = None, files=None) -> Dict[str, Any]:
    """إرسال طلب إلى Telegram API"""
    url = TELEGRAM_API_BASE + method
    try:
        if files:
            response = requests.post(url, data=params, files=files, timeout=10)
        else:
            response = requests.post(url, json=params, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Telegram API error: {e}")
        return {"ok": False, "error": str(e)}

def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    """إرسال رسالة"""
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    return tg_request("sendMessage", params)

def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    """تعديل رسالة موجودة"""
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    return tg_request("editMessageText", params)

def answer_callback(callback_query_id, text=None, alert=False):
    """الرد على Callback Query"""
    params = {
        "callback_query_id": callback_query_id,
        "show_alert": alert
    }
    if text:
        params["text"] = text
    return tg_request("answerCallbackQuery", params)

def set_webhook(webhook_url, secret_token=None):
    """تعيين Webhook"""
    params = {
        "url": webhook_url,
        "max_connections": 40,
        "allowed_updates": ["message", "callback_query"]
    }
    if secret_token:
        params["secret_token"] = secret_token
    return tg_request("setWebhook", params)

def delete_webhook():
    """حذف Webhook"""
    return tg_request("deleteWebhook")

def build_keyboard(buttons):
    """بناء لوحة مفاتيح"""
    return {
        "inline_keyboard": buttons,
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

# ================== معالجات الرسائل ==================

def handle_start(chat_id, user):
    """معالج أمر /start"""
    text = f"""
🎉 أهلاً وسهلاً بك في Worm GPT!

أنا بوت ذكي يساعدك في:
✅ الإجابة على الأسئلة
✅ توفير المعلومات
✅ حل المشاكل

📊 إحصائياتك:
• عدد الأسئلة: {user.get('questions_count', 0)}
• عدد الأسئلة المتبقية: {max(0, FREE_QUESTION_LIMIT - user.get('questions_count', 0))}

💡 الأوامر المتاحة:
/help - المساعدة
/plans - الاشتراكات المتاحة
/start - إعادة البدء
"""
    keyboard = build_keyboard([
        [{"text": "💬 اسأل سؤال", "callback_data": "new_question"}],
        [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "📚 المساعدة", "callback_data": "help"}],
        [{"text": "💳 الدفع", "callback_data": "pay_info"}, {"text": "👤 معلوماتي", "callback_data": "myinfo"}]
    ])
    send_message(chat_id, text, keyboard)

def handle_question(chat_id, user, question, keyboard):
    """معالج الأسئلة"""
    user_id = str(user.get("id"))
    
    # التحقق من حد الأسئلة المجانية
    if user.get("subscription", {}).get("active") is False:
        if user.get("questions_count", 0) >= FREE_QUESTION_LIMIT:
            send_message(chat_id, "❌ لقد استنفدت عدد الأسئلة المجانية!\n\n💳 اشترك الآن للحصول على أسئلة غير محدودة.", keyboard)
            return
    
    # إرسال رسالة التحميل
    loading_msg = send_message(chat_id, "⏳ جاري معالجة سؤالك...")
    
    try:
        # إرسال السؤال إلى API
        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "عذراً، حدث خطأ في معالجة سؤالك.")
            
            # تحديث الإحصائيات
            stats["total_questions"] += 1
            stats["successful_responses"] += 1
            user["questions_count"] = user.get("questions_count", 0) + 1
            
            # تحديث بيانات المستخدم
            users_data[user_id] = user
            save_users(users_data)
            save_stats(stats)
            
            # إرسال الإجابة
            edit_message(chat_id, loading_msg.get("result", {}).get("message_id"), answer, keyboard)
        else:
            stats["failed_responses"] += 1
            save_stats(stats)
            edit_message(chat_id, loading_msg.get("result", {}).get("message_id"), "❌ حدث خطأ في الخادم. حاول لاحقاً.", keyboard)
    except Exception as e:
        logger.error(f"Question handling error: {e}")
        stats["failed_responses"] += 1
        save_stats(stats)
        send_message(chat_id, f"❌ خطأ: {str(e)}", keyboard)

def handle_callback(callback_query):
    """معالج Callbacks"""
    callback_id = callback_query.get("id")
    chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
    data = callback_query.get("data")
    
    if not chat_id:
        return
    
    # معالجات مختلفة حسب البيانات
    if data == "new_question":
        send_message(chat_id, "📝 اكتب سؤالك:")
        answer_callback(callback_id)
    elif data == "help":
        help_text = """
📚 المساعدة والدعم

🤖 كيفية استخدام البوت:
1. اكتب سؤالك
2. سأجيب عليه فوراً
3. استمتع بالإجابة

💳 الاشتراكات:
• المجاني: 5 أسئلة فقط
• الشهري: أسئلة غير محدودة

📞 الدعم:
• WhatsApp: +20 112 030 0273
• تيليجرام: @Zi_ad_02
"""
        send_message(chat_id, help_text)
        answer_callback(callback_id)
    elif data == "plans":
        plans_text = "💳 الخطط المتاحة:\n\n"
        for code, plan in PLANS.items():
            plans_text += f"• {plan['name']}: {plan['price']} {plan['currency']}\n"
        send_message(chat_id, plans_text)
        answer_callback(callback_id)
    elif data == "myinfo":
        user = users_data.get(str(callback_query.get("from", {}).get("id")))
        if user:
            info_text = f"""
👤 معلوماتك:
• الاسم: {user.get('first_name', 'N/A')}
• المستخدم: @{user.get('username', 'N/A')}
• الأسئلة: {user.get('questions_count', 0)}
• الاشتراك: {'نعم ✅' if user.get('subscription', {}).get('active') else 'لا ❌'}
"""
            send_message(chat_id, info_text)
        answer_callback(callback_id)

def process_update(update):
    """معالجة التحديث"""
    logger.info(f"Update received: {update.get('update_id')}")
    
    # معالجة الرسائل
    if "message" in update:
        message = update["message"]
        chat_id = message.get("chat", {}).get("id")
        user_data = message.get("from", {})
        user_id = str(user_data.get("id"))
        text = message.get("text", "")
        
        # تحميل بيانات المستخدم أو إنشاء جديدة
        if user_id not in users_data:
            users_data[user_id] = {
                "id": user_id,
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name"),
                "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "questions_count": 0,
                "subscription": {"active": False}
            }
            save_users(users_data)
            stats["total_users"] += 1
            save_stats(stats)
        
        user = users_data[user_id]
        
        # معالجة الأوامر
        if text == "/start":
            handle_start(chat_id, user)
        elif text == "/help":
            send_message(chat_id, "📚 للمساعدة، اضغط على زر المساعدة أعلاه.")
        elif text == "/plans":
            plans_text = "💳 الخطط المتاحة:\n\n"
            for code, plan in PLANS.items():
                plans_text += f"• {plan['name']}: {plan['price']} {plan['currency']}\n"
            send_message(chat_id, plans_text)
        else:
            keyboard = build_keyboard([
                [{"text": "💬 سؤال آخر", "callback_data": "new_question"}],
                [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "📚 المساعدة", "callback_data": "help"}]
            ])
            handle_question(chat_id, user, text, keyboard)
    
    # معالجة الأزرار
    if "callback_query" in update:
        handle_callback(update["callback_query"])

# ================== Webhook Routes ==================

@app.route('/', methods=['GET'])
def index():
    """الصفحة الرئيسية"""
    return {
        "status": "running",
        "bot": "Worm GPT Bot",
        "version": BOT_VERSION,
        "mode": "Webhook"
    }, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """استقبال التحديثات من Telegram"""
    try:
        # التحقق من سر Webhook (اختياري لكن موصى)
        if WEBHOOK_SECRET:
            header_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
            if header_token != WEBHOOK_SECRET:
                logger.warning("Invalid webhook secret token")
                return {"ok": False}, 403
        
        # معالجة التحديث
        update = request.get_json()
        if update:
            process_update(update)
        
        return {"ok": True}, 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}, 500

@app.route('/health', methods=['GET'])
def health_check():
    """فحص صحة الخدمة"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }, 200

# ================== Start Background Workers ==================

def reminder_worker():
    """عامل التذكيرات"""
    while True:
        try:
            for user_id, user in users_data.items():
                sub = user.get("subscription", {})
                if sub.get("active"):
                    exp = datetime.strptime(sub.get("expires_at", ""), "%Y-%m-%d %H:%M:%S")
                    now = datetime.now()
                    delta = (exp - now).total_seconds() / 3600
                    
                    if 47 < delta < 49:
                        send_message(int(user_id), "⏰ اشتراكك ينتهي خلال 48 ساعة!")
                    elif 23 < delta < 25:
                        send_message(int(user_id), "⏰ اشتراكك ينتهي خلال 24 ساعة!")
            
            # النوم لمدة ساعة
            import time
            time.sleep(3600)
        except Exception as e:
            logger.error(f"Reminder worker error: {e}")
            import time
            time.sleep(60)

# ================== Initialization ==================

def setup_webhook():
    """تعيين Webhook عند بدء التطبيق"""
    if WEBHOOK_URL:
        logger.info(f"Setting webhook to {WEBHOOK_URL}")
        result = set_webhook(WEBHOOK_URL, WEBHOOK_SECRET)
        if result.get("ok"):
            logger.info("✅ Webhook set successfully!")
        else:
            logger.error(f"❌ Failed to set webhook: {result}")
    else:
        logger.warning("⚠️ WEBHOOK_URL not set. Webhook mode will not work!")

# بدء عامل التذكيرات
threading.Thread(target=reminder_worker, daemon=True).start()

if __name__ == '__main__':
    # تعيين Webhook عند البدء
    setup_webhook()
    
    # الحصول على منفذ من متغير البيئة أو استخدم 5000 كافتراضي
    port = int(os.getenv('PORT', 5000))
    
    # تشغيل تطبيق Flask
    logger.info(f"🚀 Starting Worm GPT Bot in Webhook mode on port {port}")
    print(f"🤖 البوت يعمل الآن على المنفذ {port} (Webhook mode)")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
