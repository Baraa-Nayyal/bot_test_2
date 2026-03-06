from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8495395221:AAHAlFUb28f0rY7bkhKkDZJ1plPJYXVbUyg"
ORDERS_CHAT_ID = "-1002993388534"

userState = {}

TEXT_START = """اهلاً فيك باشتراك شغوف ومبارك انك قررت تاخد خطوة تجاه البرمجة 🔥

اذا خلصت فحص 📚 وبدك تحجز مقعدك ضمن المرحلة الثانية من شغوف، تابع الخطوات مع البوت، واذا عندك استفسار ابعتلي هون @shagh1

ولتفاصيل اكتر عن نسخ شغوف ومحتواها فيك تتابع الهايلات على صفحة الإنستا ✨

هي المرحلة من شغوف مارح تقتصر فقط على النسخة الورقية من شغوف، إنما متابعة لحتى نضمن الإنجاز ان شاء الله 👀

🔸ضمن الإشتراك رح تحصل على:

🔹 ماتحس بشعور انك عم تتعلم برمجة لحالك
🔹 في حدا خبير وعنده تجربة طويلة متابعك خطوة بخطوة
🔹 حضور الكورسات ممل، إلا اذا كنت ضمن مجتمع عنده نفس الهدف
🔹 نسخة شغوف المحبوبة عند الطلاب، ولكن هالمرة شاملة لكلشي وبنفس السعر
🔹 خطة شهرية بالكورسات والعناوين يلي لازم تحضرها على حسب مستواك وهدفك
🔹 متابعة يومية ضمن كروب بيجمع طلاب بنفس الهدف
🔹 اجتماع اونلاين اسبوعي مع براء للإجابة على الاسئلة وشرح الصعب

جاهز ؟؟؟🔥
"""


TEXT_GOAL = "شو هدفك من شغوف؟"
TEXT_OLD = "هل انت من الشغوفين السابقين؟"


TEXT_INFO_OLD = """اهلين فيك 🔥

💵 سعر الاشتراك الشهري 12$

♦️ وهالدفعة حسم 50% لشهر رمضان، بصير السعر 6$ فقط

اذا مناسب الك وبدك تبدأ معنا 🧭

اكتبلي معلوماتك برسالة وحدة:
الاسم
الرقم
اسم الجامعة
السنة الدراسية

وانا رح اتواصل معك
وشكراً الك مرة تانية انك كنت جزء من رحلة شغوف 💙
"""

TEXT_INFO_NEW = """أن تصل متأخراً 😁
لاتخاف ما راح عليك شي وشغوف موجود عطول للمتابعة 🔥

💵 سعر الاشتراك الشهري متضمن نسخة شغوف كاملة: 18$

♦️ وهالدفعة حسم 50% لشهر رمضان، بصير السعر 9$ فقط

اذا مناسب الك وبدك تبدأ معنا 🧭

اكتبلي معلوماتك برسالة وحدة:
الاسم
الرقم
المحافظة
اقرب فرع قدموس الك

وانا رح اتواصل معك بخصوص الشحن والدفع
وشكراً الك انك قررت تكون جزء من رحلة شغوف 💙
"""


TEXT_INFO = """تفاصيل الاشتراك:
السعر الأساسي: {base}$
حسم رمضان: {discount}$

اكتب معلوماتك:
الاسم
المحافظة
الرقم
الموقع"""
TEXT_CONFIRM = """تأكيد الاشتراك:
{name}
{gov}
{num}
{loc}

السعر النهائي: {price}$"""
TEXT_DONE = "تم تأكيد الاشتراك ✅"
TEXT_INVALID = "الرجاء إدخال المعلومات كاملة"
TEXT_CANCEL = "تم إلغاء العملية ❌"

KB_START = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ابدأ الاشتراك 🚀", callback_data="start_sub")]]
)

KB_GOAL = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("مبتدئ وبدي امشي صح", callback_data="goal_beginner")],
        [InlineKeyboardButton("بلشت وبدي ارجع", callback_data="goal_return")],
        [InlineKeyboardButton("عندي هدف تاني", callback_data="goal_other")],
        [InlineKeyboardButton("⬅️ تراجع", callback_data="back_start")],
    ]
)

KB_OLD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("اي شغوف سابق", callback_data="old_yes")],
        [InlineKeyboardButton("لا جديد", callback_data="old_no")],
        [InlineKeyboardButton("⬅️ تراجع", callback_data="back_goal")],
    ]
)

KB_INFO = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("⬅️ تراجع", callback_data="back_goal")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel_all")],
    ]
)

KB_CONFIRM = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("تأكيد ✅", callback_data="confirm")],
        [InlineKeyboardButton("⬅️ تراجع", callback_data="back_info")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel_all")],
    ]
)

GOALS_MAP = {
    "goal_beginner": "مبتدئ وبدي امشي بالأساس صح",
    "goal_return": "بلشت باختصاص وبدي ارجع للتعلم",
    "goal_other": "هدف آخر",
}

ASK_CHAT_ID = "-1003196454615"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "بدون يوزر"
    await context.bot.send_message(
        ASK_CHAT_ID,
        f"{user.full_name}\n {username}\n",
    )
    await update.message.reply_text(TEXT_START, reply_markup=KB_START)


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    cid = q.message.chat_id
    data = q.data

    if data == "start_sub":
        userState[cid] = {}
        await q.edit_message_text(TEXT_GOAL, reply_markup=KB_GOAL)

    elif data.startswith("goal_"):
        userState[cid]["goal"] = data
        await q.edit_message_text(TEXT_OLD, reply_markup=KB_OLD)

    elif data.startswith("old_"):
        is_old = data == "old_yes"
        text = ""
        if is_old:
            base = 12
            price = 6
            await q.edit_message_text(TEXT_INFO_OLD, reply_markup=KB_INFO)
        else:
            base = 18
            price = 9
            await q.edit_message_text(TEXT_INFO_NEW, reply_markup=KB_INFO)

        userState[cid].update(
            {"old": is_old, "base": base, "price": price, "step": "info"}
        )

        await q.edit_message_text(text, reply_markup=KB_INFO)

    elif data == "back_start":
        userState.pop(cid, None)
        await q.edit_message_text(TEXT_START, reply_markup=KB_START)

    elif data == "back_goal":
        await q.edit_message_text(TEXT_GOAL, reply_markup=KB_GOAL)

    elif data == "back_info":
        s = userState[cid]
        await q.edit_message_text(
            TEXT_INFO.format(base=s["base"], discount=s["price"]), reply_markup=KB_INFO
        )

    elif data == "cancel_all":
        userState.pop(cid, None)
        await q.edit_message_text(TEXT_CANCEL, reply_markup=KB_START)

    elif data == "confirm":

        s = userState[cid]
        user = q.from_user
        username = f"@{user.username}" if user.username else f"ID: {user.id}"

        await context.bot.send_message(
            ORDERS_CHAT_ID,
            f"""طلب جديد:
            الاسم: {s['name']}
            المحافظة: {s['gov']}
            الرقم: {s['num']}
            الموقع: {s['loc']}
            الهدف: {GOALS_MAP[s['goal']]}
            شغوف سابق: {'نعم' if s['old'] else 'لا'}
            المعرف: {username}
            السعر: {s['price']}$""",
        )
        await q.edit_message_text(TEXT_DONE)
        userState.pop(cid, None)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid not in userState or userState[cid].get("step") != "info":
        return

    lines = update.message.text.split("\n")
    if len(lines) < 4:
        await update.message.reply_text(TEXT_INVALID)
        return

    name, gov, num, loc = lines[:4]
    s = userState[cid]
    s.update({"name": name, "gov": gov, "num": num, "loc": loc})

    await update.message.reply_text(
        TEXT_CONFIRM.format(
            name=name,
            gov=gov,
            num=num,
            loc=loc,
            goal=GOALS_MAP[s["goal"]],
            old="نعم" if s["old"] else "لا",
            price=s["price"],
        ),
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
