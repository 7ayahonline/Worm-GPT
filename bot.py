import logging
import requests
import time
import json
from datetime import datetime, timedelta
import os
import threading
from typing import Dict, Any

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8527079563:AAHQzGG6bQVb_f4HOUjG5o5-hYnUdH-5COk"  # تحذير: لا تنشر هذا التوكن علناً
DEVELOPER_ID = 8416721882
ADMIN_IDS = [8416721882]
API_URL = "https://worm-gpt.faresveno.workers.dev/"
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"
LOCK_FILE = "bot.lock"
BOT_VERSION = "3.0.0"
# إعدادات بايبال (ضع القيم في متغيرات البيئة لأمان أفضل)
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")
PAYPAL_ENV = os.getenv("PAYPAL_ENV", "sandbox")  # sandbox | live
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com" if PAYPAL_ENV == "sandbox" else "https://api-m.paypal.com"
PAYPAL_RECEIVE_LINK = os.getenv("PAYPAL_ME_LINK", "https://paypal.me/yourlink")

# تعريف الباقات والأسعار
# الباقات العادية والـ VIP مع أسعار تنافسية
PLANS = {
    # باقات عادية شهرية
    "monthly_eg": {"name": "شهري عادي - مصر", "price": 299, "currency": "EGP", "days": 30, "type": "عادي"},
    "monthly_int": {"name": "شهري عادي - دولي", "price": 10, "currency": "USD", "days": 30, "type": "عادي"},
    
    # باقات VIP شهرية
    "vip_monthly_eg": {"name": "شهري VIP - مصر", "price": 499, "currency": "EGP", "days": 30, "type": "VIP"},
    "vip_monthly_int": {"name": "شهري VIP - دولي", "price": 20, "currency": "USD", "days": 30, "type": "VIP"},
    
    # باقات عادية سنوية (خصم 10%)
    "yearly_eg": {"name": "سنوي عادي - مصر", "price": 3228, "original": 3588, "currency": "EGP", "days": 365, "type": "عادي", "discount": "10%"},
    "yearly_int": {"name": "سنوي عادي - دولي", "price": 108, "original": 120, "currency": "USD", "days": 365, "type": "عادي", "discount": "10%"},
    
    # باقات VIP سنوية (خصم 15%)
    "vip_yearly_eg": {"name": "سنوي VIP - مصر", "price": 5091, "original": 5988, "currency": "EGP", "days": 365, "type": "VIP", "discount": "15%"},
    "vip_yearly_int": {"name": "سنوي VIP - دولي", "price": 204, "original": 240, "currency": "USD", "days": 365, "type": "VIP", "discount": "15%"}
}

# عدد الأسئلة المجانية قبل الاشتراك
FREE_QUESTION_LIMIT = 5

# ملف لحفظ الإحصائيات
STATS_FILE = "bot_stats.json"
USERS_FILE = "users_data.json"
ADMIN_LOG_FILE = "admin_actions.json"
COUPONS_FILE = "coupons.json"

# تحميل الإحصائيات
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # ضمان وجود حقول جديدة
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

# تحميل بيانات المستخدمين
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

stats = load_stats()
users_data = load_users()
def load_coupons():
    if os.path.exists(COUPONS_FILE):
        try:
            with open(COUPONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_coupons(entries):
    with open(COUPONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

coupons_store = load_coupons()

# تحميل سجل الإجراءات الإدارية
def load_admin_log():
    if os.path.exists(ADMIN_LOG_FILE):
        try:
            with open(ADMIN_LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_admin_log(entries):
    with open(ADMIN_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

admin_actions = load_admin_log()

def log_admin_action(actor_id: int, action: str, details: str):
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor_id,
        "action": action,
        "details": details
    }
    admin_actions.append(entry)
    # احتفظ بآخر 500 فقط لتجنب التضخم
    if len(admin_actions) > 500:
        admin_actions[:] = admin_actions[-500:]
    save_admin_log(admin_actions)

# ===== إدارة الكوبونات =====
def find_coupon(code: str):
    code_l = (code or '').lower().strip()
    for c in coupons_store:
        if (c.get('code','').lower() == code_l):
            return c
    return None

def create_coupon(code: str, plan: str, dtype: str, value: float, max_uses: int, expires_days: int, notes: str = ""):
    if find_coupon(code):
        return False, "الكوبون موجود بالفعل"
    expires_at = None
    if expires_days and expires_days > 0:
        expires_at = (datetime.now() + timedelta(days=expires_days)).strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "code": code,
        "plan": plan or "any",
        "discountType": dtype,  # percent | amount | extend_days | extra_free
        "discountValue": value,
        "maxUses": max_uses,
        "usedCount": 0,
        "expiresAt": expires_at,
        "active": True,
        "notes": notes or ""
    }
    coupons_store.append(entry)
    save_coupons(coupons_store)
    log_admin_action(DEVELOPER_ID, "coupon_create", f"{entry}")
    return True, "✅ تم إنشاء الكوبون"

def set_coupon_active(code: str, active: bool):
    c = find_coupon(code)
    if not c:
        return False, "❌ لم يتم العثور على الكوبون"
    c['active'] = bool(active)
    save_coupons(coupons_store)
    log_admin_action(DEVELOPER_ID, "coupon_set_active", f"{code} → {active}")
    return True, "✅ تم تحديث حالة الكوبون"

def coupon_list_text():
    if not coupons_store:
        return "لا توجد كوبونات حالياً"
    lines = ["🎟️ <b>قائمة الكوبونات</b>\n"]
    for c in coupons_store:
        lines.append(
            f"• {c['code']} | خطة: {c.get('plan','any')} | نوع: {c['discountType']}={c['discountValue']} | "
            f"مستخدم: {c.get('usedCount',0)}/{c.get('maxUses',0)} | فعال: {c.get('active',False)} | انتهاء: {c.get('expiresAt','لا يوجد')}"
        )
    return "\n".join(lines)

def coupon_info_text(code: str):
    c = find_coupon(code)
    if not c:
        return "❌ لم يتم العثور على الكوبون"
    return (
        f"🎟️ كوبون: <b>{c['code']}</b>\n"
        f"الخطة: {c.get('plan','any')}\n"
        f"النوع: {c['discountType']}\n"
        f"القيمة: {c['discountValue']}\n"
        f"الاستخدامات: {c.get('usedCount',0)}/{c.get('maxUses',0)}\n"
        f"نشط: {c.get('active',False)}\n"
        f"ينتهي: {c.get('expiresAt','لا يوجد')}\n"
        f"ملاحظات: {c.get('notes','-')}"
    )

def resolve_user_id(identifier: str) -> str:
    """يحاول تحويل إدخال (آيدي رقمي أو @يوزر) إلى آيدي المستخدم كسلسلة.
    يعيد None إذا لم يتم العثور عليه."""
    ident = identifier.strip()
    # إذا رقم خالص
    if ident.isdigit():
        return ident if ident in users_data else None
    # إذا @يوزر
    if ident.startswith('@'):
        uname = ident[1:].strip().lower()
        for uid, data in users_data.items():
            if (data.get('username') or '').lower() == uname:
                return uid
        return None
    return None

def get_ai_response(question: str) -> dict:
    try:
        response = requests.get(API_URL, params={"text": question}, timeout=30)
        response.raise_for_status()
        return {"success": True, "result": response.json().get("result", "معنديش رد ليك!")}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "انتهت مهلة الطلب. حاول مرة أخرى."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"خطأ في الاتصال: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"حدث خطأ غير متوقع: {str(e)}"}

def tg_request(method: str, params: Dict[str, Any] = None, json_body: Dict[str, Any] = None) -> Dict[str, Any]:
    url = TELEGRAM_API_BASE + method
    try:
        if json_body is not None:
            r = requests.post(url, json=json_body, timeout=30)
        else:
            r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if not data.get("ok", False):
            logger.error(f"Telegram API error in {method}: {data}")
        return data
    except Exception as e:
        logger.error(f"Telegram request failed ({method}): {e}")
        return {"ok": False, "error": str(e)}

def send_message(chat_id: int, text: str, reply_markup: Dict[str, Any] = None, parse_mode: str = "HTML"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "disable_web_page_preview": True}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return tg_request("sendMessage", json_body=payload)

def edit_message(chat_id: int, message_id: int, text: str, reply_markup: Dict[str, Any] = None, parse_mode: str = "HTML"):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return tg_request("editMessageText", json_body=payload)

def answer_callback(callback_query_id: str):
    tg_request("answerCallbackQuery", params={"callback_query_id": callback_query_id})

def build_keyboard(button_rows):
    return {"inline_keyboard": button_rows}

# ===== نظام الاشتراكات المتميز =====
def premium_subscription_message() -> str:
    """الرسالة الترويجية الاحترافية لنظام الاشتراكات"""
    return """╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║           🌟 مرحباً بك في عالم Worm GPT المتميز والاحترافي 🌟             ║
║                                                                           ║
║                    نظام الاشتراكات الراقي والشامل                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ <b>نعم، أنت الآن على بوابة أفضل خدمة ذكاء اصطناعي في المنطقة!</b>

نحن نقدم لك <i>نظام اشتراكات متكاملاً</i> تم تصميمه بعناية من قبل خبراء
لتوفير <b>أفضل تجربة استخدام</b> مع <b>أعلى جودة خدمة</b> وأكثرها راحة.

اختر الخطة التي تناسب احتياجاتك، واستمتع بـ:
   ✓ دعم فني متواصل 24/7
   ✓ ردود سريعة وذكية جداً
   ✓ تحديثات يومية للميزات
   ✓ أمان عالي لبياناتك
   ✓ واجهة سهلة وسلسة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 <b>الخطط المتاحة:</b>

🟢 <b>الباقة العادية</b> – مثالية للمستخدمين العاديين
   ✓ أسئلة غير محدودة | ✓ دعم سريع | ✓ تحديثات منتظمة

⭐ <b>الباقة VIP</b> – للمحترفين والشركات
   ✓ أسئلة غير محدودة مع أولويات عالية | ✓ دعم VIP حصري | ✓ ميزات متقدمة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>الأسعار الشهرية:</b>
🇪🇬 عادي: 299 EGP | VIP: 499 EGP
🌐 عادي: 10 USD | VIP: 20 USD

🎁 <b>الأسعار السنوية (خصومات ضخمة):</b>
🇪🇬 عادي: 3,228 EGP ⬇️ (من 3,588) | VIP: 5,091 EGP ⬇️ (من 5,988)
🌐 عادي: 108 USD ⬇️ (من 120) | VIP: 204 USD ⬇️ (من 240)

💳 <b>طرق دفع موثوقة:</b>
داخل مصر: فودافون كاش | اتصالات كاش | تحويل بنكي
دولي: PayPal | Stripe | Visa/Card | Binance Pay

✅ <b>الخطوة التالية:</b>
اختر الخطة التي تناسبك من الأزرار أدناه وابدأ الآن!

🎯 <i>استثمر في الجودة، استثمر في نفسك!</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

def create_main_keyboard():
    """لوحة مفاتيح الرئيسية"""
    return build_keyboard([
        [{"text": "📚 المساعدة", "callback_data": "help"}, {"text": "📊 الإحصائيات", "callback_data": "stats"}],
        [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
        [{"text": "👤 معلوماتي", "callback_data": "myinfo"}],
        [{"text": "👨‍💻 المطور", "url": "https://t.me/Zi_ad_02"}, {"text": "🤖 قناة البوت", "callback_data": "channel"}],
        [{"text": "📞 واتساب الدعم", "url": "https://wa.me/201120300273"}]
    ])

def create_help_keyboard():
    """لوحة مفاتيح المساعدة"""
    return build_keyboard([
        [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 طرق الدفع", "callback_data": "pay_info"}],
        [{"text": "❓ أسئلة شائعة", "callback_data": "sub_faq"}, {"text": "📞 تواصل", "url": "https://t.me/Zi_ad_02"}],
        [{"text": "🏠 العودة", "callback_data": "main_menu"}]
    ])

def create_premium_subscription_keyboard():
    """إنشاء لوحة مفاتيح الاشتراكات المتميزة مع جميع الخيارات"""
    keyboard = build_keyboard([
        # الشهري المصري
        [
            {"text": "🟢 شهري - 299 EGP", "callback_data": "sub_monthly_eg_std"},
            {"text": "⭐ VIP شهري - 499 EGP", "callback_data": "sub_monthly_eg_vip"}
        ],
        # الشهري الدولي
        [
            {"text": "🟢 شهري - 10 USD", "callback_data": "sub_monthly_int_std"},
            {"text": "⭐ VIP شهري - 20 USD", "callback_data": "sub_monthly_int_vip"}
        ],
        # السنوي المصري
        [
            {"text": "🎁 سنوي - 3,228 EGP", "callback_data": "sub_yearly_eg_std"},
            {"text": "🎁 VIP سنوي - 5,091 EGP", "callback_data": "sub_yearly_eg_vip"}
        ],
        # السنوي الدولي
        [
            {"text": "🎁 سنوي - 108 USD", "callback_data": "sub_yearly_int_std"},
            {"text": "🎁 VIP سنوي - 204 USD", "callback_data": "sub_yearly_int_vip"}
        ],
        # أزرار إضافية
        [
            {"text": "💳 طرق الدفع", "callback_data": "sub_payment_methods"},
            {"text": "❓ الأسئلة الشائعة", "callback_data": "sub_faq"}
        ],
        [
            {"text": "💬 تواصل معنا", "url": "https://t.me/Zi_ad_02"},
            {"text": "🏠 الرئيسية", "callback_data": "main_menu"}
        ]
    ])
    return keyboard

def create_payment_methods_keyboard(plan_code: str = None):
    """لوحة مفاتيح طرق الدفع"""
    if plan_code:
        return build_keyboard([
            [{"text": "🔵 PayPal", "callback_data": f"pay_paypal:{plan_code}"}],
            [{"text": "💳 Stripe/Card", "callback_data": f"pay_card:{plan_code}"}],
            [{"text": "💰 محافظ رقمية", "callback_data": f"pay_wallet:{plan_code}"}],
            [{"text": "📱 فودافون/اتصالات", "callback_data": f"pay_mobile:{plan_code}"}],
            [{"text": "🏦 تحويل بنكي", "callback_data": f"pay_bank:{plan_code}"}],
            [{"text": "⬅️ العودة", "callback_data": "plans"}]
        ])
    else:
        return build_keyboard([
            [{"text": "📦 الخطط", "callback_data": "plans"}],
            [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
        ])

def handle_premium_subscription_callback(callback: Dict[str, Any]):
    """معالج شامل لجميع خيارات الاشتراكات المتميزة"""
    data = callback.get("data")
    cq_id = callback.get("id")
    message = callback.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    message_id = message.get("message_id")
    user = callback.get("from", {})
    
    answer_callback(cq_id)
    
    if not chat_id or not message_id:
        return
    
    # معلومات الاشتراكات
    sub_info = {
        "sub_monthly_eg_std": {"name": "شهري عادي - مصر", "price": "299", "currency": "EGP", "type": "std", "region": "🇪🇬"},
        "sub_monthly_eg_vip": {"name": "شهري VIP - مصر", "price": "499", "currency": "EGP", "type": "vip", "region": "🇪🇬"},
        "sub_monthly_int_std": {"name": "شهري عادي - دولي", "price": "10", "currency": "USD", "type": "std", "region": "🌐"},
        "sub_monthly_int_vip": {"name": "شهري VIP - دولي", "price": "20", "currency": "USD", "type": "vip", "region": "🌐"},
        "sub_yearly_eg_std": {"name": "سنوي عادي - مصر", "price": "3,228", "currency": "EGP", "type": "std", "region": "🇪🇬", "savings": "360"},
        "sub_yearly_eg_vip": {"name": "سنوي VIP - مصر", "price": "5,091", "currency": "EGP", "type": "vip", "region": "🇪🇬", "savings": "897"},
        "sub_yearly_int_std": {"name": "سنوي عادي - دولي", "price": "108", "currency": "USD", "type": "std", "region": "🌐", "savings": "12"},
        "sub_yearly_int_vip": {"name": "سنوي VIP - دولي", "price": "204", "currency": "USD", "type": "vip", "region": "🌐", "savings": "36"}
    }
    
    if data.startswith("sub_") and data in sub_info:
        sub = sub_info[data]
        badge = "⭐" if sub["type"] == "vip" else "🟢"
        msg_lines = [
            f"{badge} <b>{sub['name']}</b> {sub['region']}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"💰 السعر: <code>{sub['price']} {sub['currency']}</code>",
        ]
        
        if "savings" in sub:
            msg_lines.append(f"🎉 توفير: {sub['savings']} {sub['currency']}")
        
        msg_lines.extend([
            "",
            "<b>📋 المميزات:</b>",
            "✓ أسئلة غير محدودة",
            "✓ دعم متواصل 24/7",
            "✓ تحديثات يومية",
            "✓ أمان عالي"
        ])
        
        if sub["type"] == "vip":
            msg_lines.extend(["✓ أولويات عالية", "✓ ميزات حصرية", "✓ مستشار شخصي"])
        
        msg_lines.append("\n👇 اختر طريقة الدفع:")
        
        payment_kb = build_keyboard([
            [{"text": "🔵 PayPal", "callback_data": f"pay_paypal:{data}"}],
            [{"text": "💳 Stripe/Card", "callback_data": f"pay_card:{data}"}],
            [{"text": "💰 المحافظ الرقمية", "callback_data": f"pay_wallet:{data}"}],
            [{"text": "📱 فودافون/اتصالات", "callback_data": f"pay_mobile:{data}"}],
            [{"text": "🏦 تحويل بنكي", "callback_data": f"pay_bank:{data}"}],
            [{"text": "⬅️ العودة", "callback_data": "sub_back"}]
        ])
        
        edit_message(chat_id, message_id, "\n".join(msg_lines), reply_markup=payment_kb)
    
    elif data == "sub_payment_methods":
        payment_text = (
            "💳 <b>طرق الدفع المتاحة</b>\n\n"
            "🇪🇬 <b>داخل مصر:</b>\n"
            "  📱 فودافون كاش\n"
            "  📱 اتصالات كاش\n"
            "  📱 أورانج كاش\n"
            "  💰 محافظ رقمية\n"
            "  🏦 تحويل بنكي\n\n"
            "🌐 <b>دولي:</b>\n"
            "  🔵 PayPal\n"
            "  💳 Stripe\n"
            "  💳 Visa/MasterCard\n"
            "  ₿ Binance Pay\n"
            "  🏦 تحويل بنكي دولي\n\n"
            "📞 للمساعدة: @Zi_ad_02"
        )
        kb = build_keyboard([
            [{"text": "⬅️ عودة", "callback_data": "sub_back"}],
            [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
        ])
        edit_message(chat_id, message_id, payment_text, reply_markup=kb)
    
    elif data == "sub_faq":
        faq_text = (
            "❓ <b>الأسئلة الشائعة</b>\n\n"
            "<b>س: هل يمكن إلغاء الاشتراك؟</b>\n"
            "ج: نعم، بدون غرامات في أي وقت.\n\n"
            "<b>س: الفرق بين العادي و VIP؟</b>\n"
            "ج: VIP بأولويات عالية ودعم مخصص وميزات حصرية.\n\n"
            "<b>س: هل هناك ضمان؟</b>\n"
            "ج: نعم، ضمان 100% في أول 7 أيام.\n\n"
            "<b>س: عدد الأسئلة المسموحة؟</b>\n"
            "ج: غير محدود! سؤل متى تشاء.\n\n"
            "<b>س: هل البيانات آمنة؟</b>\n"
            "ج: نعم، تشفير عسكري من الدرجة الأولى.\n\n"
            "📞 سؤال آخر؟ تواصل: @Zi_ad_02"
        )
        kb = build_keyboard([
            [{"text": "⬅️ عودة", "callback_data": "sub_back"}]
        ])
        edit_message(chat_id, message_id, faq_text, reply_markup=kb)
    
    elif data == "sub_back":
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, premium_subscription_message(), reply_markup=kb)
    
    # معالجات طرق الدفع
    elif data.startswith("pay_paypal:"):
        plan_code = data.split(":", 1)[1]
        if plan_code not in PLANS:
            return
        p = PLANS[plan_code]
        currency = p.get("currency")
        price = p.get("price")
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, (
            "🔵 <b>الدفع عبر PayPal</b>\n\n"
            f"📦 الباقة: {p['name']}\n"
            f"💵 السعر: {price} {currency}\n\n"
            f"🔗 <b>رابط الدفع:</b> <code>{PAYPAL_RECEIVE_LINK}</code>\n\n"
            "📝 <b>خطوات الدفع:</b>\n"
            "1. انسخ الرابط أعلاه\n"
            "2. افتحه في المتصفح\n"
            "3. أكمل عملية الدفع\n"
            "4. انسخ رمز العملية (Capture ID)\n"
            "5. أرسل: /confirm_pay CAPTURE_ID\n\n"
            "❓ <b>بحاجة للمساعدة؟</b>\n"
            "📞 تواصل: @Zi_ad_02 أو +20 112 030 0273"
        ), reply_markup=kb)
    
    elif data.startswith("pay_card:"):
        plan_code = data.split(":", 1)[1]
        if plan_code not in PLANS:
            return
        p = PLANS[plan_code]
        currency = p.get("currency")
        price = p.get("price")
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, (
            "💳 <b>الدفع ببطاقة ائتمان (Stripe)</b>\n\n"
            f"📦 الباقة: {p['name']}\n"
            f"💵 السعر: {price} {currency}\n\n"
            "📝 <b>الطريقة:</b>\n"
            "1. تواصل مع المطور @Zi_ad_02\n"
            "2. سيتم إرسالك رابط الدفع الآمن\n"
            "3. أدخل بيانات بطاقتك بأمان\n"
            "4. ستتلقى تأكيد الدفع فوراً\n\n"
            "🛡️ <b>أمان:</b> تشفير من الدرجة الأولى\n"
            "✅ <b>الدعم:</b> 24/7\n\n"
            "📞 تواصل الآن: @Zi_ad_02 أو +20 112 030 0273"
        ), reply_markup=kb)
    
    elif data.startswith("pay_wallet:"):
        plan_code = data.split(":", 1)[1]
        if plan_code not in PLANS:
            return
        p = PLANS[plan_code]
        currency = p.get("currency")
        price = p.get("price")
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, (
            "💰 <b>الدفع عبر المحافظ الرقمية</b>\n\n"
            f"📦 الباقة: {p['name']}\n"
            f"💵 السعر: {price} {currency}\n\n"
            "🔗 <b>الخيارات المتاحة:</b>\n"
            "📱 Google Pay\n"
            "🍎 Apple Pay\n"
            "💳 Samsung Pay\n"
            "💱 منصات الدفع الأخرى\n\n"
            "📝 <b>الطريقة:</b>\n"
            "تواصل مع المطور لإرسال رابط الدفع الآمن\n\n"
            "📞 تواصل: @Zi_ad_02\n"
            "☎️ WhatsApp: +20 112 030 0273"
        ), reply_markup=kb)
    
    elif data.startswith("pay_mobile:"):
        plan_code = data.split(":", 1)[1]
        if plan_code not in PLANS:
            return
        p = PLANS[plan_code]
        price = p.get("price")
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, (
            "📱 <b>الدفع عبر الشركات المحمول</b>\n\n"
            f"📦 الباقة: {p['name']}\n"
            f"💵 السعر: {price} جنيه\n\n"
            "🟠 <b>فودافون كاش:</b>\n"
            "أرسل رسالة *688# ثم اتبع التعليمات\n\n"
            "🔵 <b>اتصالات كاش:</b>\n"
            "أرسل رسالة *110# ثم اتبع التعليمات\n\n"
            "🟡 <b>أورانج كاش:</b>\n"
            "أرسل رسالة *888# ثم اتبع التعليمات\n\n"
            "📝 <b>بعد الدفع:</b>\n"
            "أخبرنا برقم المرجعية (Reference)\n\n"
            "📞 تواصل: @Zi_ad_02\n"
            "☎️ WhatsApp: +20 112 030 0273"
        ), reply_markup=kb)
    
    elif data.startswith("pay_bank:"):
        plan_code = data.split(":", 1)[1]
        if plan_code not in PLANS:
            return
        p = PLANS[plan_code]
        price = p.get("price")
        currency = p.get("currency")
        kb = create_premium_subscription_keyboard()
        
        if currency == "EGP":
            bank_info = (
                "🏦 <b>التحويل البنكي (مصر)</b>\n\n"
                f"📦 الباقة: {p['name']}\n"
                f"💵 السعر: {price} جنيه\n\n"
                "📋 <b>بيانات التحويل:</b>\n"
                "البنك: [سيتم إرسالها عند طلب التحويل]\n"
                "الحساب: [سيتم إرسالها عند طلب التحويل]\n"
                "الرقم الدولي: [سيتم إرسالها عند طلب التحويل]\n\n"
                "📝 <b>الطريقة:</b>\n"
                "1. تواصل مع المطور\n"
                "2. ستحصل على بيانات التحويل الكاملة\n"
                "3. قم بالتحويل من حسابك\n"
                "4. أخبرنا برقم المرجعية\n\n"
                "⏱️ وقت التفعيل: في غضون 24 ساعة\n\n"
                "📞 تواصل: @Zi_ad_02\n"
                "☎️ WhatsApp: +20 112 030 0273"
            )
        else:
            bank_info = (
                "🏦 <b>التحويل البنكي الدولي</b>\n\n"
                f"📦 الباقة: {p['name']}\n"
                f"💵 السعر: {price} {currency}\n\n"
                "🌐 <b>الخيارات:</b>\n"
                "• SWIFT Transfer\n"
                "• Wire Transfer\n"
                "• International Bank Transfer\n\n"
                "📝 <b>الطريقة:</b>\n"
                "تواصل مع المطور للحصول على بيانات التحويل الدولية\n\n"
                "📞 تواصل: @Zi_ad_02\n"
                "☎️ WhatsApp: +20 112 030 0273"
            )
        
        edit_message(chat_id, message_id, bank_info, reply_markup=kb)

# ===== PayPal Helpers =====
def paypal_get_access_token() -> str:
    if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET:
        return ""
    try:
        r = requests.post(
            f"{PAYPAL_API_BASE}/v1/oauth2/token",
            data={"grant_type":"client_credentials"},
            auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
            timeout=30
        )
        r.raise_for_status()
        return r.json().get("access_token", "")
    except Exception as e:
        logger.error(f"PayPal token error: {e}")
        return ""

def paypal_get_capture(capture_id: str) -> Dict[str, Any]:
    token = paypal_get_access_token()
    if not token:
        return {"ok": False, "error": "no_token"}
    try:
        r = requests.get(
            f"{PAYPAL_API_BASE}/v2/payments/captures/{capture_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        if r.status_code == 200:
            return {"ok": True, "data": r.json()}
        return {"ok": False, "status": r.status_code, "data": r.json()}
    except Exception as e:
        logger.error(f"PayPal capture error: {e}")
        return {"ok": False, "error": str(e)}

def handle_start(user: Dict[str, Any], chat_id: int):
    user_id = str(user.get("id"))
    if user_id not in users_data:
        users_data[user_id] = {
            "username": user.get("username") or "بدون معرف",
            "first_name": user.get("first_name") or "مستخدم",
            "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "questions_count": 0,
            "subscription": {
                "active": False,
                "plan_code": None,
                "expires_at": None,
                "free_remaining": FREE_QUESTION_LIMIT
            }
        }
        stats["total_users"] += 1
        save_users(users_data)
        save_stats(stats)
    # ضمان وجود بنية الاشتراك
    sub = users_data[user_id].setdefault("subscription", {
        "active": False,
        "plan_code": None,
        "expires_at": None,
        "free_remaining": FREE_QUESTION_LIMIT
    })
    keyboard = create_main_keyboard()
    if sub.get("active"):
        plan_name = PLANS.get(sub.get("plan_code"), {}).get("name", "باقة غير معروفة")
        welcome_message = (
            f"🌟 مرحباً بك {user.get('first_name')}! 🌟\n\n"
            "✅ اشتراكك نشط\n"
            f"📦 الباقة: {plan_name}\n"
            f"⏰ ينتهي في: {sub.get('expires_at')}\n\n"
            "أرسل سؤالك الآن واستمتع بالاستخدام غير المحدود! 🚀\n"
            "━━━━━━━━━━━━━━━"
        )
    else:
        welcome_message = (
            f"🌟 مرحباً بك {user.get('first_name')}! 🌟\n\n"
            "🚨 <b>مطلوب اشتراك للاستخدام غير المحدود</b>\n"
            f"🎁 الأسئلة المجانية المتبقية: {sub.get('free_remaining', 0)} / {FREE_QUESTION_LIMIT}\n\n"
            "استخدم /plans لمعرفة الباقات المتاحة\n"
            "ثم /subscribe لمعرفة طريقة الطلب والتفعيل.\n\n"
            "✨ خلال الفترة المجانية يمكنك تجربة الذكاء الاصطناعي بالسؤال مباشرة.\n"
            "━━━━━━━━━━━━━━━"
        )
    send_message(chat_id, welcome_message, reply_markup=keyboard)

def help_text():
    return (
        "📚 <b>دليل استخدام البوت</b> 📚\n\n"
        "🔹 <b>الأوامر المتاحة:</b>\n\n"
        "/start - بدء البوت والترحيب\n"
        "/help - عرض هذه المساعدة\n"
        "/stats - عرض إحصائيات البوت\n"
        "/about - معلومات عن البوت\n"
        "/myinfo - معلوماتك الشخصية\n\n"
        "🔹 <b>كيفية الاستخدام:</b>\n\n"
        "1️⃣ أرسل أي سؤال مباشرة\n2️⃣ انتظر الرد\n3️⃣ اسأل أكثر\n\n"
        "🔹 <b>أمثلة:</b>\n• ما هي عاصمة مصر؟\n• اكتب قصة قصيرة\n• كيف أتعلم البرمجة؟\n• ما هو الذكاء الاصطناعي؟\n\n"
        "━━━━━━━━━━━━━━━\n👨‍💻 المطور: @Zi_ad_02\n📞 واتساب الدعم: +20 112 030 0273\n💳 الدفع: /pay <plan_code> ثم /confirm_pay <capture_id>\n━━━━━━━━━━━━━━━"
    )

def version_text():
    return (
        f"🧩 <b>إصدار البوت:</b> <code>{BOT_VERSION}</code>\n"
        f"🕒 وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "📦 الميزات: إدارة، اشتراكات، موافقات، تذكيرات، تقارير أسبوعية"
    )

def stats_text():
    return (
        "📊 <b>إحصائيات البوت</b> 📊\n\n"
        f"👥 عدد المستخدمين: <code>{stats['total_users']}</code>\n"
        f"❓ إجمالي الأسئلة: <code>{stats['total_questions']}</code>\n"
        f"✅ ناجحة: <code>{stats['successful_responses']}</code>\n"
        f"❌ فاشلة: <code>{stats['failed_responses']}</code>\n"
        f"📈 نسبة النجاح: <code>{(stats['successful_responses'] / max(stats['total_questions'], 1) * 100):.1f}%</code>\n\n"
        f"⏰ التحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "━━━━━━━━━━━━━━━"
    )

def about_text():
    return (
        "ℹ️ <b>معلومات عن البوت</b> ℹ️\n\n"
        "🤖 <b>الاسم:</b> Worm GPT Bot\n"
        "🔖 <b>الإصدار:</b> 2.0 Professional\n"
        "📅 <b>الإطلاق:</b> 2025\n\n"
        "💫 <b>المميزات:</b>\n✓ ذكاء اصطناعي متقدم\n✓ ردود سريعة\n✓ دعم العربية\n✓ واجهة سهلة\n✓ تحديثات مستمرة\n\n"
        "🛠️ <b>التقنيات:</b> Python + Requests + Worm GPT API + JSON\n\n"
        "👨‍💻 المطور: @Zi_ad_02\n🆔 المعرف: @Ts_6_Bot\n📞 واتساب الدعم: +20 112 030 0273\n"
        "━━━━━━━━━━━━━━━"
    )

def myinfo_text(user):
    user_id = str(user.get("id"))
    if user_id in users_data:
        info = users_data[user_id]
        sub = info.get("subscription", {})
        status = "✅ نشط" if sub.get("active") else (f"🔄 مجاني - متبقي {sub.get('free_remaining', 0)}" if sub.get("free_remaining") else "❌ غير مشترك")
        plan_name = PLANS.get(sub.get("plan_code"), {}).get("name") if sub.get("plan_code") else "-"
        return (
            "👤 <b>معلوماتك</b> 👤\n\n"
            f"🆔 الآيدي: <code>{user.get('id')}</code>\n"
            f"👤 الاسم: {user.get('first_name')}\n"
            f"📛 المعرف: @{user.get('username') or 'بدون معرف'}\n"
            f"📅 الانضمام: {info['joined_date']}\n"
            f"❓ الأسئلة: {info['questions_count']}\n"
            f"💳 الاشتراك: {status}\n"
            f"📦 الباقة: {plan_name}\n"
            f"⏰ انتهاء: {sub.get('expires_at') or '-'}\n"
            "━━━━━━━━━━━━━━━"
        )
    return "❌ لم يتم العثور على بياناتك. استخدم /start أولاً."

def handle_broadcast(text: str, chat_id: int, user_id: int):
    if user_id not in ADMIN_IDS:
        send_message(chat_id, "⛔ هذا الأمر متاح للمطورين فقط!")
        return
    msg = text.replace("/broadcast", "", 1).strip()
    if not msg:
        send_message(chat_id, "📢 الاستخدام: /broadcast رسالتك")
        return
    send_message(chat_id, "📤 جاري الإرسال ...")
    success = 0
    fail = 0
    for uid in list(users_data.keys()):
        try:
            send_message(int(uid), f"📢 <b>رسالة من المطور:</b>\n\n{msg}")
            success += 1
        except Exception as e:
            logger.error(f"فشل إرسال إلى {uid}: {e}")
            fail += 1
        time.sleep(0.05)
    send_message(chat_id, f"✅ تم الإرسال\nنجاح: {success}\nفشل: {fail}")
    log_admin_action(user_id, "broadcast", f"نجاح: {success} فشل: {fail}")

def handle_admin(chat_id: int, user_id: int):
    if user_id not in ADMIN_IDS:
        send_message(chat_id, "⛔ أمر إداري فقط")
        return
    keyboard = build_keyboard([
        [{"text": "📥 الطلبات المعلقة", "callback_data": "admin_pending"}, {"text": "👥 المستخدمون", "callback_data": "admin_users"}],
        [{"text": "📊 الإحصائيات", "callback_data": "admin_stats"}, {"text": "🧾 السجل", "callback_data": "admin_logs"}],
        [{"text": "🎟️ الكوبونات", "callback_data": "admin_coupons"}],
        [{"text": "🔄 تحديث", "callback_data": "admin_menu"}]
    ])
    send_message(chat_id, "🛠️ <b>لوحة الإدارة</b>\nاختر إجراء:", reply_markup=keyboard)

def handle_request(chat_id: int, user: Dict[str, Any], full_text: str):
    user_id = str(user.get("id"))
    parts = full_text.split()
    if len(parts) < 2:
        send_message(chat_id, "الاستخدام: /request <plan_code> [ملاحظات]")
        return
    plan_code = parts[1].strip()
    notes = " ".join(parts[2:]).strip() if len(parts) > 2 else ""
    if plan_code not in PLANS:
        send_message(chat_id, "❌ كود باقة غير صحيح. استخدم /plans")
        return
    # حفظ الطلب للمراجعة
    u = users_data.setdefault(user_id, {})
    pending = {
        "plan_code": plan_code,
        "notes": notes,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    u["pending_request"] = pending
    save_users(users_data)
    send_message(chat_id, f"✅ تم تسجيل طلبك للباقه {plan_code}. سيتم مراجعته من قبل الإدارة.")
    # إشعار الإدارة
    for aid in ADMIN_IDS:
        try:
            send_message(aid, f"📥 طلب اشتراك جديد من {user.get('first_name')} (@{user.get('username')})\nالباقة: {plan_code}\nملاحظات: {notes or '-'}\nآيدي: {user_id}\nاستخدم /activate {user_id} {plan_code}")
        except:
            pass

def list_pending_requests() -> str:
    lines = ["📥 <b>الطلبات المعلقة</b>\n"]
    count = 0
    for uid, data in users_data.items():
        pending = data.get("pending_request")
        if pending:
            count += 1
            lines.append(f"• {data.get('first_name')} (@{data.get('username')}) → {pending['plan_code']} في {pending['time']} (آيدي: {uid})")
    if count == 0:
        lines.append("لا توجد طلبات حالياً.")
    else:
        lines.append("\nاضغط زر الموافقة بجوار الطلب أو استخدم /activate")
    return "\n".join(lines)

def view_admin_logs() -> str:
    lines = ["🧾 <b>آخر 20 إجراء إداري</b>\n"]
    for entry in admin_actions[-20:]:
        lines.append(f"• {entry['time']} - {entry['actor']} - {entry['action']} → {entry['details']}")
    if len(lines) == 1:
        lines.append("لا يوجد سجلات بعد.")
    return "\n".join(lines)

def handle_revoke(chat_id: int, user_id: int, target_id: str):
    if user_id not in ADMIN_IDS:
        send_message(chat_id, "⛔ أمر إداري فقط")
        return
    if target_id not in users_data:
        send_message(chat_id, "❌ مستخدم غير موجود")
        return
    sub = users_data[target_id].setdefault("subscription", {})
    if not sub.get("active"):
        send_message(chat_id, "المستخدم غير مشترك بالفعل")
        return
    sub.update({"active": False, "plan_code": None, "expires_at": None, "free_remaining": FREE_QUESTION_LIMIT})
    # إزالة الطلب المعلق لو وجد
    users_data[target_id].pop("pending_request", None)
    save_users(users_data)
    send_message(chat_id, "✅ تم إلغاء الاشتراك")
    try:
        send_message(int(target_id), "⚠️ تم إلغاء اشتراكك. يمكنك استخدام الأسئلة المجانية ثم الاشتراك مجدداً.")
    except:
        pass
    log_admin_action(user_id, "revoke", f"إلغاء اشتراك للمستخدم {target_id}")

def handle_users(chat_id: int, user_id: int):
    if user_id not in ADMIN_IDS:
        send_message(chat_id, "⛔ هذا الأمر للمطور فقط")
        return
    out = "👥 <b>أول 20 مستخدم:</b>\n\n"
    for uid, data in list(users_data.items())[:20]:
        out += f"• {data['first_name']} (@{data['username']}) - {data['questions_count']} سؤال\n"
    out += f"\n📊 الإجمالي: {len(users_data)}"
    # إضافة لوحة فلترة بسيطة حسب الخطة
    plan_opts = []
    for code, p in PLANS.items():
        plan_opts.append([{"text": p['name'], "callback_data": f"filter_plan:{code}"}])
    kb = build_keyboard(plan_opts[:6] + [[{"text":"🏠 إدارة","callback_data":"admin_menu"}]])
    send_message(chat_id, out, reply_markup=kb)

def handle_question(chat_id: int, user: Dict[str, Any], text: str, reply_keyboard: Dict[str, Any] = None):
    user_id = str(user.get("id"))
    if user_id in users_data:
        users_data[user_id]["questions_count"] += 1
        # التحقق من الاشتراك
        sub = users_data[user_id].setdefault("subscription", {
            "active": False,
            "plan_code": None,
            "expires_at": None,
            "free_remaining": FREE_QUESTION_LIMIT
        })
        # إذا غير نشط نستخدم الأسئلة المجانية
        if not sub.get("active"):
            remaining = sub.get("free_remaining", 0)
            if remaining <= 0:
                kb = build_keyboard([
                    [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
                    [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                ])
                send_message(chat_id, (
                    "🚫 <b>ليس لديك اشتراك نشط</b>\n"
                    f"انتهى حد الأسئلة المجانية ({FREE_QUESTION_LIMIT}).\n"
                    "استخدم /plans لمشاهدة الباقات و /subscribe لطلب اشتراك."
                ), reply_markup=kb)
                return
            else:
                sub["free_remaining"] = remaining - 1
        save_users(users_data)
    waiting = send_message(chat_id, "⏳ جاري البحث عن الإجابة...")
    message_id = None
    try:
        message_id = waiting.get("result", {}).get("message_id") if waiting.get("ok") else None
    except:
        pass
    response = get_ai_response(text)
    stats["total_questions"] += 1
    if response["success"]:
        stats["successful_responses"] += 1
        if reply_keyboard is None:
            reply_keyboard = build_keyboard([
                [{"text": "❓ سؤال جديد", "callback_data": "new_question"}, {"text": "📊 الإحصائيات", "callback_data": "stats"}],
                [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
                [{"text": "📚 المساعدة", "callback_data": "help"}, {"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
            ])
        result = f"💬 <b>السؤال:</b>\n{text}\n\n✨ <b>الإجابة:</b>\n{response['result']}"
        if message_id:
            edit_message(chat_id, message_id, result, reply_markup=reply_keyboard)
        else:
            send_message(chat_id, result, reply_markup=reply_keyboard)
    else:
        stats["failed_responses"] += 1
        kb = build_keyboard([
            [{"text": "🔄 حاول مجددا", "callback_data": "new_question"}],
            [{"text": "💬 تواصل المطور", "url": "https://t.me/Zi_ad_02"}],
            [{"text": "📚 المساعدة", "callback_data": "help"}, {"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
        ])
        err = f"❌ خطأ:\n{response['error']}\n\n💡 حاول ثانية أو راسل المطور @Zi_ad_02"
        if message_id:
            edit_message(chat_id, message_id, err, reply_markup=kb)
        else:
            send_message(chat_id, err, reply_markup=kb)
    save_stats(stats)

def reminder_worker():
    while True:
        try:
            now = datetime.now()
            for uid, data in users_data.items():
                sub = data.get("subscription") or {}
                if sub.get("active") and sub.get("expires_at"):
                    try:
                        exp = datetime.strptime(sub["expires_at"], "%Y-%m-%d %H:%M:%S")
                    except:
                        continue
                    # 48 ساعة قبل الانتهاء ولم يُرسل تذكير
                    if exp - now <= timedelta(hours=48) and not sub.get("reminder_sent"):
                        try:
                            send_message(int(uid), f"⏰ تذكير: سينتهي اشتراكك في {sub['expires_at']}. راسل المطور للتمديد.")
                            sub["reminder_sent"] = True
                            save_users(users_data)
                        except:
                            pass
                    # 24 ساعة قبل الانتهاء ولم يُرسل تذكير 24h
                    if exp - now <= timedelta(hours=24) and not sub.get("reminder24_sent"):
                        try:
                            send_message(int(uid), f"⏰ تذكير أخير: متبقي أقل من 24 ساعة على انتهاء اشتراكك ({sub['expires_at']}).")
                            sub["reminder24_sent"] = True
                            save_users(users_data)
                        except:
                            pass
            time.sleep(1800)  # فحص كل 30 دقيقة
        except Exception as e:
            logger.error(f"Reminder worker error: {e}")
            time.sleep(1800)

def weekly_report_worker():
    # يرسل تقريراً أسبوعياً كل يوم أحد صباحاً
    while True:
        try:
            now = datetime.now()
            # يوم الأحد (weekday=6) في الساعة 10:00 تقريباً
            week_id = f"{now.year}-W{now.isocalendar().week}"
            if now.weekday() == 6 and now.hour == 10 and (stats.get("last_week_report_week") != week_id):
                # حساب ملخص بسيط
                active = 0
                expired = 0
                for _, data in users_data.items():
                    sub = data.get("subscription") or {}
                    if sub.get("active"):
                        try:
                            exp = datetime.strptime(sub.get("expires_at"), "%Y-%m-%d %H:%M:%S")
                        except:
                            exp = now
                        if exp >= now:
                            active += 1
                        else:
                            expired += 1
                msg = (
                    "📈 <b>تقرير أسبوعي</b>\n\n"
                    f"👥 المستخدمون: {len(users_data)}\n"
                    f"❓ الأسئلة الإجمالية: {stats.get('total_questions',0)}\n"
                    f"✅ ناجحة: {stats.get('successful_responses',0)} | ❌ فاشلة: {stats.get('failed_responses',0)}\n"
                    f"🟢 اشتراكات نشطة: {active} | 🔴 منتهية: {expired}"
                )
                for aid in ADMIN_IDS:
                    try:
                        send_message(aid, msg)
                    except:
                        pass
                stats["last_week_report_week"] = week_id
                save_stats(stats)
                # انتظر قليلاً لمنع إرسال مكرر أثناء نفس الساعة
                time.sleep(3600)
            time.sleep(300)
        except Exception as e:
            logger.error(f"Weekly report worker error: {e}")
            time.sleep(600)

def handle_callback(callback: Dict[str, Any]):
    data = callback.get("data")
    cq_id = callback.get("id")
    message = callback.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    message_id = message.get("message_id")
    answer_callback(cq_id)
    if not chat_id or not message_id:
        return
    
    # معالج الاشتراكات المتميزة والدفع الأساسي
    if data and (data.startswith("sub_") or data.startswith("pay_paypal:") or data.startswith("pay_card:") or 
                 data.startswith("pay_wallet:") or data.startswith("pay_mobile:") or data.startswith("pay_bank:")):
        handle_premium_subscription_callback(callback)
        return
    
    if data == "help":
        keyboard = create_help_keyboard()
        edit_message(chat_id, message_id, help_text(), reply_markup=keyboard)
    elif data == "about":
        keyboard = create_help_keyboard()
        edit_message(chat_id, message_id, about_text(), reply_markup=keyboard)
    elif data == "version":
        kb = build_keyboard([[{"text": "🏠 العودة", "callback_data": "main_menu"}]])
        edit_message(chat_id, message_id, version_text(), reply_markup=kb)
    elif data == "stats":
        keyboard = build_keyboard([[{"text": "🏠 العودة", "callback_data": "main_menu"}]])
        edit_message(chat_id, message_id, stats_text(), reply_markup=keyboard)
    elif data == "plans":
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, premium_subscription_message(), reply_markup=kb)
    elif data == "plans":
        kb = create_premium_subscription_keyboard()
        edit_message(chat_id, message_id, premium_subscription_message(), reply_markup=kb)
    elif data == "pay_info":
        kb = create_payment_methods_keyboard()
        edit_message(chat_id, message_id, (
            "💳 <b>طرق الدفع المتاحة</b>\n\n"
            "🇪🇬 <b>داخل مصر:</b>\n"
            "  📱 فودافون كاش\n"
            "  📱 اتصالات كاش\n"
            "  📱 أورانج كاش\n"
            "  💰 محافظ رقمية (Google Pay، Apple Pay)\n"
            "  🏦 تحويل بنكي\n\n"
            "🌐 <b>دولي:</b>\n"
            "  🔵 PayPal\n"
            "  💳 Stripe\n"
            "  💳 Visa/MasterCard\n"
            "  ₿ Binance Pay\n"
            "  🏦 تحويل بنكي دولي\n\n"
            f"📞 <b>للمساعدة:</b> @Zi_ad_02 أو +20 112 030 0273"
        ), reply_markup=kb)
    elif data == "channel":
        kb = build_keyboard([
            [{"text": "🔗 انضم للقناة", "url": "https://t.me/Ts_6_Bot"}],
            [{"text": "👨‍💻 المطور", "url": "https://t.me/Zi_ad_02"}],
            [{"text": "🏠 العودة", "callback_data": "main_menu"}]
        ])
        edit_message(chat_id, message_id, (
            "📢 <b>قنوات وحسابات البوت</b>\n\n"
            "🤖 <b>البوت الرسمي:</b>\n"
            "🔗 @Ts_6_Bot\n\n"
            "👨‍💻 <b>المطور والدعم:</b>\n"
            "📱 @Zi_ad_02\n"
            "☎️ WhatsApp: +20 112 030 0273\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "انضم للتحديثات والعروض الخاصة 🚀"
        ), reply_markup=kb)
    elif data == "new_question":
        edit_message(chat_id, message_id, "❓ أرسل سؤالك الجديد الآن!")
    elif data == "main_menu":
        keyboard = create_main_keyboard()
        edit_message(chat_id, message_id, "🏠 <b>القائمة الرئيسية</b>\n\nاختر خيار أو أرسل سؤالك مباشرة👇", reply_markup=keyboard)
    elif data == "myinfo":
        user_from = callback.get("from", {})
        kb = build_keyboard([[{"text":"📦 الخطط","callback_data":"plans"}, {"text":"💳 الدفع","callback_data":"pay_info"}],[{"text":"🏠 العودة","callback_data":"main_menu"}]])
        edit_message(chat_id, message_id, myinfo_text(user_from), reply_markup=kb)
    # قسم الإدارة عبر الأزرار
    elif data == "admin_menu":
        handle_admin(chat_id, callback.get("from", {}).get("id"))
    elif data == "admin_pending":
        # بناء أزرار موافقة لكل طلب (حتى 10)
        pending_rows = []
        shown = 0
        for uid, data in users_data.items():
            if shown >= 10:
                break
            p = data.get("pending_request")
            if p:
                shown += 1
                btn_text = f"✅ موافقة: @{data.get('username')} → {p['plan_code']}"
                pending_rows.append([{ "text": btn_text, "callback_data": f"approve:{uid}:{p['plan_code']}" }])
        # أضف زر إلغاء بجانب الموافقة
        if pending_rows:
            rows = []
            for r in pending_rows:
                btn = r[0]
                cb = btn.get("callback_data", "")
                parts = cb.split(":")
                uid = parts[1] if len(parts) > 2 else None
                if uid:
                    rows.append([btn, {"text": "⛔ إلغاء", "callback_data": f"revoke:{uid}"}])
                else:
                    rows.append([btn])
            kb = build_keyboard(rows)
        else:
            kb = build_keyboard([[{"text":"لا توجد طلبات","callback_data":"admin_menu"}]])
        edit_message(chat_id, message_id, list_pending_requests(), reply_markup=kb)
    elif data and data.startswith("approve:"):
        # approve:user_id:plan_code
        try:
            _, uid, plan_code = data.split(":", 2)
        except:
            uid = None; plan_code = None
        if not uid or plan_code not in PLANS:
            edit_message(chat_id, message_id, "❌ بيانات موافقة غير صالحة")
            return
        # تنفيذ التفعيل
        if uid not in users_data:
            edit_message(chat_id, message_id, "❌ المستخدم غير موجود")
            return
        days = PLANS[plan_code]["days"]
        expires = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        users_data[uid]["subscription"] = {
            "active": True,
            "plan_code": plan_code,
            "expires_at": expires,
            "free_remaining": 0,
            "reminder_sent": False
        }
        users_data[uid].pop("pending_request", None)
        save_users(users_data)
        log_admin_action(callback.get("from",{}).get("id"), "approve", f"خطة {plan_code} للمستخدم {uid}")
        edit_message(chat_id, message_id, f"✅ تم تفعيل {plan_code} للمستخدم {uid} حتى {expires}")
        try:
            send_message(int(uid), f"🎉 تم تفعيل اشتراكك: {PLANS[plan_code]['name']} حتى {expires}")
        except:
            pass
    elif data == "admin_logs":
        edit_message(chat_id, message_id, view_admin_logs())
    elif data == "admin_stats":
        edit_message(chat_id, message_id, stats_text())
    elif data == "admin_users":
        # إعادة استخدام الوظيفة الحالية
        handle_users(chat_id, callback.get("from", {}).get("id"))
    elif data == "admin_coupons":
        kb = build_keyboard([
            [{"text": "📜 قائمة الكوبونات", "callback_data": "coupon_list"}],
            [{"text": "🚫 تعطيل كوبون", "callback_data": "coupon_disable_prompt"}, {"text": "✅ تفعيل كوبون", "callback_data": "coupon_enable_prompt"}],
            [{"text": "🏠 إدارة", "callback_data": "admin_menu"}]
        ])
        edit_message(chat_id, message_id, "🎟️ إدارة الكوبونات:\nاستخدم الأوامر الإدارية لإنشاء كوبون جديد:\n/coupon_create CODE PLAN TYPE VALUE MAXUSES EXPIRESDAYS [NOTES]", reply_markup=kb)
    elif data == "coupon_list":
        edit_message(chat_id, message_id, coupon_list_text())
    elif data == "coupon_disable_prompt":
        edit_message(chat_id, message_id, "أرسل: /coupon_disable CODE")
    elif data == "coupon_enable_prompt":
        edit_message(chat_id, message_id, "أرسل: /coupon_enable CODE")
    elif data and data.startswith("filter_plan:"):
        plan_code = data.split(":",1)[1]
        matches = []
        for uid, info in users_data.items():
            sub = info.get("subscription", {})
            if sub.get("plan_code") == plan_code and sub.get("active"):
                matches.append(f"• {info.get('first_name')} (@{info.get('username')}) → ينتهي {sub.get('expires_at')} (آيدي: {uid})")
        text = (
            f"🔎 <b>مستخدمو الباقة:</b> {PLANS.get(plan_code,{}).get('name','-')}\n\n" +
            ("\n".join(matches) if matches else "لا يوجد مشتركون نشطون لهذه الباقة.")
        )
        kb = build_keyboard([[{"text":"🏠 إدارة","callback_data":"admin_menu"}]])
        edit_message(chat_id, message_id, text, reply_markup=kb)
    elif data and data.startswith("extend7:"):
        uid = data.split(":",1)[1] if ":" in data else None
        if not uid:
            edit_message(chat_id, message_id, "❌ بيانات تمديد غير صالحة")
            return
        actor = callback.get("from",{}).get("id")
        if actor not in ADMIN_IDS:
            edit_message(chat_id, message_id, "⛔ غير مسموح")
            return
        sub = users_data.setdefault(uid, {}).setdefault("subscription", {})
        if not sub.get("active"):
            edit_message(chat_id, message_id, "❌ المستخدم غير مشترك")
            return
        try:
            current_exp = datetime.strptime(sub.get("expires_at"), "%Y-%m-%d %H:%M:%S")
        except:
            current_exp = datetime.now()
        new_exp = (current_exp + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        sub["expires_at"] = new_exp
        save_users(users_data)
        log_admin_action(actor, "extend", f"تمديد 7 أيام للمستخدم {uid} حتى {new_exp}")
        edit_message(chat_id, message_id, f"✅ تم تمديد اشتراك المستخدم {uid} حتى {new_exp}")
        try:
            send_message(int(uid), f"🔄 تم تمديد اشتراكك 7 أيام إضافية حتى {new_exp}")
        except:
            pass
    elif data and data.startswith("revoke:"):
        uid = data.split(":", 1)[1] if ":" in data else None
        if not uid:
            edit_message(chat_id, message_id, "❌ بيانات إلغاء غير صالحة")
            return
        handle_revoke(chat_id, callback.get("from",{}).get("id"), uid)
        edit_message(chat_id, message_id, f"✅ تم إلغاء اشتراك المستخدم {uid}")

def process_update(update: Dict[str, Any]):
    # معالجة الرسائل العادية
    if "message" in update:
        msg = update["message"]
        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        text = msg.get("text", "")
        user = msg.get("from", {})
        if not chat_id or not text:
            return
        if text.startswith("/start"):
            handle_start(user, chat_id)
        elif text.startswith("/help"):
            keyboard = create_help_keyboard()
            send_message(chat_id, help_text(), reply_markup=keyboard)
        elif text.startswith("/version"):
            keyboard = build_keyboard([[{"text": "🏠 العودة", "callback_data": "main_menu"}]])
            send_message(chat_id, version_text(), reply_markup=keyboard)
        elif text.startswith("/stats"):
            keyboard = build_keyboard([
                [{"text": "🏠 العودة", "callback_data": "main_menu"}]
            ])
            send_message(chat_id, stats_text(), reply_markup=keyboard)
        elif text.startswith("/about"):
            keyboard = create_help_keyboard()
            send_message(chat_id, about_text(), reply_markup=keyboard)
        elif text.startswith("/myinfo"):
            keyboard = build_keyboard([
                [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
                [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
            ])
            send_message(chat_id, myinfo_text(user), reply_markup=keyboard)
        elif text.startswith("/menu"):
            keyboard = create_main_keyboard()
            send_message(chat_id, "🏠 <b>القائمة الرئيسية</b>\n\nاختر خيار أو أرسل سؤالك مباشرة👇", reply_markup=keyboard)
        elif text.startswith("/plans"):
            kb = create_premium_subscription_keyboard()
            send_message(chat_id, premium_subscription_message(), reply_markup=kb)
        elif text.startswith("/subscribe"):
            kb = create_premium_subscription_keyboard()
            send_message(chat_id, premium_subscription_message(), reply_markup=kb)
        elif text.startswith("/pay"):
            parts = text.split()
            if len(parts) < 2:
                keyboard = build_keyboard([
                    [{"text": "📦 الخطط", "callback_data": "plans"}],
                    [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                ])
                send_message(chat_id, "الاستخدام: /pay <plan_code>", reply_markup=keyboard)
            else:
                plan_code = parts[1]
                if plan_code not in PLANS:
                    keyboard = build_keyboard([
                        [{"text": "📦 الخطط", "callback_data": "plans"}],
                        [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                    ])
                    send_message(chat_id, "❌ كود باقة غير صحيح. استخدم /plans", reply_markup=keyboard)
                else:
                    p = PLANS[plan_code]
                    currency = p.get("currency")
                    price = p.get("price")
                    keyboard = build_keyboard([
                        [{"text": "🔵 PayPal", "callback_data": f"pay_paypal:{plan_code}"}],
                        [{"text": "💳 Stripe/Card", "callback_data": f"pay_card:{plan_code}"}],
                        [{"text": "💰 محافظ رقمية", "callback_data": f"pay_wallet:{plan_code}"}],
                        [{"text": "📱 فودافون/اتصالات", "callback_data": f"pay_mobile:{plan_code}"}],
                        [{"text": "🏦 تحويل بنكي", "callback_data": f"pay_bank:{plan_code}"}],
                        [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                    ])
                    send_message(
                        chat_id,
                        (
                            "💳 <b>الدفع عبر بايبال</b>\n\n"
                            f"📦 الباقة: {p['name']}\n💵 السعر: {price} {currency}\n\n"
                            f"🔗 ادفع هنا: {PAYPAL_RECEIVE_LINK}\n"
                            "ثم بعد الدفع، أرسل رمز عملية التحصيل (capture_id) عبر:\n"
                            "<code>/confirm_pay CAPTURE_ID</code>\n\n"
                            "ملاحظة: الدفع التلقائي تجريبي وقد يحتاج مراجعة يدوية."
                        ),
                        reply_markup=keyboard
                    )
        elif text.startswith("/confirm_pay"):
            parts = text.split()
            if len(parts) < 2:
                keyboard = build_keyboard([
                    [{"text": "💳 طرق الدفع", "callback_data": "sub_payment_methods"}],
                    [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                ])
                send_message(chat_id, "الاستخدام: /confirm_pay <capture_id>", reply_markup=keyboard)
            else:
                capture_id = parts[1]
                res = paypal_get_capture(capture_id)
                if not res.get("ok"):
                    keyboard = build_keyboard([
                        [{"text": "💳 طرق الدفع", "callback_data": "sub_payment_methods"}],
                        [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                    ])
                    send_message(chat_id, "❌ فشل التحقق من الدفع أو لا توجد صلاحيات API", reply_markup=keyboard)
                else:
                    data = res.get("data", {})
                    status = data.get("status")
                    amount = data.get("amount", {}).get("value")
                    currency = data.get("amount", {}).get("currency_code")
                    payer = data.get("payer", {}).get("name", {}).get("given_name")
                    keyboard = build_keyboard([
                        [{"text": "📦 الخطط", "callback_data": "plans"}],
                        [{"text": "💬 تواصل الإدارة", "url": "https://t.me/Zi_ad_02"}],
                        [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
                    ])
                    if status == "COMPLETED":
                        send_message(chat_id, (
                            "✅ تم تأكيد الدفع من بايبال.\n"
                            f"الحالة: {status}\nالقيمة: {amount} {currency}\n"
                            f"الدافع: {payer or '-'}\n\n"
                            "راسل الإدارة لتحديد الباقة أو استخدم /request مع كود الباقة ليتم تفعيلها."
                        ), reply_markup=keyboard)
                        log_admin_action(DEVELOPER_ID, "paypal_confirm", f"capture {capture_id} for chat {chat_id} amount {amount} {currency}")
                    else:
                        send_message(chat_id, f"⚠️ حالة الدفع: {status}. يرجى التأكد وإعادة المحاولة.", reply_markup=keyboard)
        elif text.startswith("/coupon"):
            parts = text.split()
            if len(parts) < 2:
                send_message(chat_id, "الاستخدام: /coupon <code>")
            else:
                code = parts[1].strip()
                c = find_coupon(code)
                if not c:
                    send_message(chat_id, "❌ كوبون غير صالح")
                else:
                    if not c.get('active', False):
                        send_message(chat_id, "⛔ الكوبون غير مفعل حالياً")
                        return
                    # تحقق انتهاء
                    exp = c.get('expiresAt')
                    if exp:
                        try:
                            if datetime.now() > datetime.strptime(exp, "%Y-%m-%d %H:%M:%S"):
                                send_message(chat_id, "⏰ انتهت صلاحية الكوبون")
                                return
                        except:
                            pass
                    # حدود الاستخدام
                    if c.get('maxUses',0) > 0 and c.get('usedCount',0) >= c.get('maxUses',0):
                        send_message(chat_id, "📛 تم الوصول لأقصى عدد استخدامات لهذا الكوبون")
                        return
                    user_id_s = str(user.get("id"))
                    sub = users_data.setdefault(user_id_s, {}).setdefault("subscription", {})
                    dtype = c.get('discountType')
                    val = c.get('discountValue', 0)
                    # دعم أنواع متعددة: extend_days للمشتركين، extra_free لغير المشتركين، percent/amount للعرض فقط
                    if dtype == 'extend_days' and sub.get("active") and sub.get("expires_at"):
                        try:
                            current_exp = datetime.strptime(sub.get("expires_at"), "%Y-%m-%d %H:%M:%S")
                        except:
                            current_exp = datetime.now()
                        new_exp = (current_exp + timedelta(days=int(val))).strftime("%Y-%m-%d %H:%M:%S")
                        sub["expires_at"] = new_exp
                        save_users(users_data)
                        send_message(chat_id, f"🎟️ تم تطبيق الكوبون. تمديد {int(val)} يوم حتى {new_exp}")
                    elif dtype == 'extra_free' and not sub.get("active"):
                        extra = int(val)
                        current_free = sub.get("free_remaining", FREE_QUESTION_LIMIT)
                        sub["free_remaining"] = current_free + extra
                        save_users(users_data)
                        send_message(chat_id, f"🎟️ تم تطبيق الكوبون. أسئلة مجانية إضافية +{extra} (المتبقي: {sub['free_remaining']})")
                    elif dtype in ('percent','amount'):
                        send_message(chat_id, "✅ تم التحقق من الكوبون. سيتم احتساب الخصم عند الدفع.")
                    else:
                        send_message(chat_id, "✅ تم التحقق من الكوبون.")
                    # تسجيل استخدام
                    c['usedCount'] = int(c.get('usedCount',0)) + 1
                    save_coupons(coupons_store)
                    log_admin_action(DEVELOPER_ID, "coupon_used", f"{code} للمستخدم {user_id_s}")
        elif text.startswith("/status"):
            keyboard = build_keyboard([
                [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
                [{"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
            ])
            send_message(chat_id, myinfo_text(user), reply_markup=keyboard)
        elif text.startswith("/request"):
            handle_request(chat_id, user, text)
        elif text.startswith("/admin"):
            handle_admin(chat_id, user.get("id"))
        elif text.startswith("/coupon_create"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 7:
                    send_message(chat_id, "الاستخدام: /coupon_create CODE PLAN TYPE(percent|amount|extend_days|extra_free) VALUE MAXUSES EXPIRESDAYS [NOTES]")
                else:
                    _, code, plan, dtype, value, maxuses, expdays, *notes = parts
                    try:
                        value = float(value)
                        maxuses = int(maxuses)
                        expdays = int(expdays)
                    except:
                        send_message(chat_id, "❌ قيمة/عدد/أيام غير صحيحة")
                        return
                    if dtype not in ("percent","amount","extend_days","extra_free"):
                        send_message(chat_id, "❌ النوع يجب أن يكون percent أو amount أو extend_days أو extra_free")
                        return
                    ok, msg = create_coupon(code, plan, dtype, value, maxuses, expdays, " ".join(notes) if notes else "")
                    send_message(chat_id, msg)
        elif text.startswith("/coupon_disable"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 2:
                    send_message(chat_id, "الاستخدام: /coupon_disable CODE")
                else:
                    _, code = parts[:2]
                    ok, msg = set_coupon_active(code, False)
                    send_message(chat_id, msg)
        elif text.startswith("/coupon_enable"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 2:
                    send_message(chat_id, "الاستخدام: /coupon_enable CODE")
                else:
                    _, code = parts[:2]
                    ok, msg = set_coupon_active(code, True)
                    send_message(chat_id, msg)
        elif text.startswith("/coupon_list"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                send_message(chat_id, coupon_list_text())
        elif text.startswith("/coupon_info"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 2:
                    send_message(chat_id, "الاستخدام: /coupon_info CODE")
                else:
                    _, code = parts[:2]
                    send_message(chat_id, coupon_info_text(code))
        elif text.startswith("/activate"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 3:
                    send_message(chat_id, "الاستخدام: /activate <user_id|@username> <plan_code> [days]")
                else:
                    target_id = resolve_user_id(parts[1])
                    plan_code = parts[2]
                    override_days = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None
                    if not target_id:
                        send_message(chat_id, "❌ المستخدم غير موجود بالآيدي/اليوزر")
                    elif plan_code not in PLANS:
                        send_message(chat_id, "❌ كود الباقة غير صحيح")
                    else:
                        days = override_days or PLANS[plan_code]["days"]
                        expires = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
                        users_data[target_id]["subscription"] = {
                            "active": True,
                            "plan_code": plan_code,
                            "expires_at": expires,
                            "free_remaining": 0
                        }
                        # إزالة الطلب المعلق بعد التفعيل
                        users_data[target_id].pop("pending_request", None)
                        save_users(users_data)
                        send_message(chat_id, f"✅ تم تفعيل الباقة {plan_code} للمستخدم {target_id} حتى {expires}")
                        try:
                            send_message(int(target_id), f"🎉 تم تفعيل اشتراكك بنجاح! الباقة: {PLANS[plan_code]['name']} حتى {expires}")
                        except:
                            pass
                        log_admin_action(user.get("id"), "activate", f"خطة {plan_code} للمستخدم {target_id} حتى {expires}")
        elif text.startswith("/revoke"):
            parts = text.split()
            if len(parts) < 2:
                send_message(chat_id, "الاستخدام: /revoke <user_id|@username>")
            else:
                target_id = resolve_user_id(parts[1])
                if not target_id:
                    send_message(chat_id, "❌ المستخدم غير موجود بالآيدي/اليوزر")
                else:
                    handle_revoke(chat_id, user.get("id"), target_id)
        elif text.startswith("/extend"):
            if user.get("id") not in ADMIN_IDS:
                send_message(chat_id, "⛔ أمر إداري فقط")
            else:
                parts = text.split()
                if len(parts) < 3:
                    send_message(chat_id, "الاستخدام: /extend <user_id|@username> <extra_days>")
                else:
                    target_id = resolve_user_id(parts[1])
                    extra_days = int(parts[2]) if parts[2].isdigit() else 0
                    if not target_id:
                        send_message(chat_id, "❌ المستخدم غير موجود بالآيدي/اليوزر")
                    else:
                        sub = users_data[target_id].setdefault("subscription", {})
                        if not sub.get("active"):
                            send_message(chat_id, "❌ المستخدم غير مشترك حالياً")
                        else:
                            try:
                                current_exp = datetime.strptime(sub.get("expires_at"), "%Y-%m-%d %H:%M:%S")
                            except:
                                current_exp = datetime.now()
                            new_exp = (current_exp + timedelta(days=extra_days)).strftime("%Y-%m-%d %H:%M:%S")
                            sub["expires_at"] = new_exp
                            save_users(users_data)
                            send_message(chat_id, f"✅ تم تمديد الاشتراك حتى {new_exp}")
                            try:
                                send_message(int(target_id), f"🔄 تم تمديد اشتراكك حتى {new_exp}")
                            except:
                                pass
                            log_admin_action(user.get("id"), "extend", f"تمديد {extra_days} يوم للمستخدم {target_id} حتى {new_exp}")
        elif text.startswith("/broadcast"):
            handle_broadcast(text, chat_id, user.get("id"))
        elif text.startswith("/users"):
            handle_users(chat_id, user.get("id"))
        else:
            keyboard = build_keyboard([
                [{"text": "💬 سؤال آخر", "callback_data": "new_question"}],
                [{"text": "📦 الخطط", "callback_data": "plans"}, {"text": "💳 الدفع", "callback_data": "pay_info"}],
                [{"text": "📚 المساعدة", "callback_data": "help"}, {"text": "🏠 الرئيسية", "callback_data": "main_menu"}]
            ])
            handle_question(chat_id, user, text, keyboard)
    # معالجة الضغط على الأزرار
    if "callback_query" in update:
        handle_callback(update["callback_query"])

def polling_loop():
    logger.info("🚀 بدء البوت (وضع يدوي بدون مكتبة) ...")
    print("🤖 البوت يعمل الآن (Polling يدوي) - Ctrl+C للإيقاف")
    # إزالة أي Webhook لتجنب التعارض
    try:
        tg_request("deleteWebhook")
    except Exception as e:
        logger.warning(f"deleteWebhook failed: {e}")
    # بدء خيط التذكير
    try:
        threading.Thread(target=reminder_worker, daemon=True).start()
    except Exception as e:
        logger.warning(f"Reminder thread start failed: {e}")
    # بدء خيط التقرير الأسبوعي
    try:
        threading.Thread(target=weekly_report_worker, daemon=True).start()
    except Exception as e:
        logger.warning(f"Weekly report thread start failed: {e}")
    offset = None
    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            data = tg_request("getUpdates", params=params)
            if data.get("ok"):
                for upd in data.get("result", []):
                    offset = upd.get("update_id", 0) + 1
                    process_update(upd)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("🛑 تم إيقاف البوت يدوياً.")
            break
        except Exception as e:
            logger.error(f"حلقة التحديث فشلت: {e}")
            time.sleep(2)

if __name__ == '__main__':
    # حارس مثيل واحد بسيط: إذا كان الملف موجوداً، لا يبدأ مثيل جديد
    try:
        if os.path.exists(LOCK_FILE):
            print("⚠️ يوجد مثيل آخر يعمل (bot.lock موجود). إنهاء التشغيل لتجنب التعارض.")
        else:
            with open(LOCK_FILE, 'w', encoding='utf-8') as f:
                f.write(str(os.getpid()))
            try:
                polling_loop()
            finally:
                try:
                    os.remove(LOCK_FILE)
                except:
                    pass
    except Exception as e:
        logger.error(f"Lock guard error: {e}")
