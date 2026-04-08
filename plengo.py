from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8228308595:AAEFsqA0x7BgKeDiMFkXYIhWJq5pTB9CfpU"
ORDERS_CHAT_ID = "-5055774658"

userState = {}

TEXT_START = """❤️‍🔥 سمات العلوم للصف التاسع والبكالوريا ❤️‍🔥

📚 300 العلوم صارت ب جيبك 🙂‍↔️‼️

✨ صار فيك تضمن رسمات العلوم مع بلينغو
حطينالك كل الرسمات رما نقصنا ولا رسمة

📦 علبة طلاب البكالوريا: 103 كروت
📦 علبة التاسع: 86 كروت

🛍️ متوفر:
- كرتون 🎁
- ورقي 📄

💰 الأسعار:

🎓 بكالوريا:
- كرتون: 60 ألف
- ورقي: 35 ألف

📘 تاسع:
- كرتون: 55 ألف
- ورقي: 27 ألف

➕ إضافة ورقي مع علبة كرتون: +4500

للاستفسار على 
@Diana_Tarabishi

📩 اضغط متابعة واطلب نسختك الآن 🔥
"""

KB_START = InlineKeyboardMarkup(
    [[InlineKeyboardButton("متابعة 🛒", callback_data="start")]]
)

KB_TYPE = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("بكالوريا", callback_data="bac")],
        [InlineKeyboardButton("تاسع", callback_data="grade9")],
    ]
)

KB_VERSION = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("كرتون", callback_data="carton")],
        [InlineKeyboardButton("ورقي", callback_data="paper")],
        [InlineKeyboardButton("علبة كرتونئ + ورقي", callback_data="both")],
    ]
)

KB_LOCATION = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("حلب", callback_data="aleppo")],
        [InlineKeyboardButton("محافظات", callback_data="other")],
    ]
)

KB_CONFIRM = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("تأكيد ✅", callback_data="confirm")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel")],
    ]
)

PRICES = {
    "bac_carton": 60000,
    "bac_paper": 35000,
    "grade9_carton": 55000,
    "grade9_paper": 27000,
    "extra": 4500,
}


def calculate_price(s):
    base = 0
    key = f"{s['type']}_{s['version']}" if s["version"] != "both" else None

    if s["version"] == "both":
        if s["type"] == "bac":
            base = PRICES["bac_carton"] + PRICES["bac_paper"] + PRICES["extra"]
        else:
            base = PRICES["grade9_carton"] + PRICES["grade9_paper"] + PRICES["extra"]
    else:
        base = PRICES[key]

    return base


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEXT_START, reply_markup=KB_START)


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cid = q.from_user.id
    data = q.data

    if data == "start":
        userState[cid] = {}
        await q.edit_message_text("اختر المرحلة:", reply_markup=KB_TYPE)

    elif data in ["bac", "grade9"]:
        userState[cid]["type"] = data
        await q.edit_message_text("اختر النسخة:", reply_markup=KB_VERSION)

    elif data in ["carton", "paper", "both"]:
        userState[cid]["version"] = data
        await q.edit_message_text("حدد موقعك:", reply_markup=KB_LOCATION)

    elif data in ["aleppo", "other"]:
        userState[cid]["location"] = data
        userState[cid]["step"] = "info"

        if data == "aleppo":
            await q.edit_message_text("ابعت معلوماتك:\nالاسم\nالرقم")
        else:
            await q.edit_message_text(
                "ابعت معلوماتك:\nالاسم\nالرقم\nالمحافظة\nالفرع (قدموس/الهرم)"
            )

    elif data == "confirm":
        s = userState[cid]
        user = q.from_user
        username = f"@{user.username}" if user.username else f"ID: {user.id}"

        price = calculate_price(s)

        await context.bot.send_message(
            ORDERS_CHAT_ID,
            f"""طلب جديد 📦

الاسم: {s['name']}
الرقم: {s['phone']}
الموقع: {s.get('gov', 'حلب')}
الفرع: {s.get('branch', '-')}

المرحلة: {s['type']}
النسخة: {s['version']}

السعر: {price}

المعرف: {username}
""",
        )

        await q.edit_message_text("تم تسجيل طلبك ✅")
        userState.pop(cid, None)

    elif data == "cancel":
        userState.pop(cid, None)
        await q.edit_message_text("تم الإلغاء ❌")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id

    if cid not in userState or userState[cid].get("step") != "info":
        return

    text = update.message.text.split("\n")
    s = userState[cid]

    if s["location"] == "aleppo":
        if len(text) < 2:
            await update.message.reply_text("الرجاء إدخال المعلومات كاملة")
            return

        name, phone = text[:2]
        s.update({"name": name, "phone": phone})

    else:
        if len(text) < 4:
            await update.message.reply_text("الرجاء إدخال المعلومات كاملة")
            return

        name, phone, gov, branch = text[:4]
        s.update({"name": name, "phone": phone, "gov": gov, "branch": branch})

    price = calculate_price(s)

    await update.message.reply_text(
        f"""تأكيد الطلب:

الاسم: {s['name']}
الرقم: {s['phone']}

السعر: {price}
""",
        reply_markup=KB_CONFIRM,
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
