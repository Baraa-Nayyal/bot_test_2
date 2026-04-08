from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8366088074:AAEzceCNbGjnmq6S-E9rstLBvXcZKwDNhg8"
ORDERS_CHAT_ID = "-1002993388534"
ASK_CHAT_ID = "-1003196454615"

userState = {}

TEXT_START = """اشتراك شغوف الدفعة الرابعة 🔥

الدفعة مخصصة فقط للفرونت إيند، مهما كان مستواك رح نتأكد من ترميم الأساسيات ونكمل ببناء المشاريع.

بناء مشاريع html css بشكل سريع لأن هي المرحلة أخدها ال ai ولكن لازم نتأكد انه نحن منعرف نبني أي تصميم ويب.

- نتعلم جافاسكربت بكورس سريع وبعدها نطبق 5 مشاريع صغيرة وسريعة انا مصورها ومع كل مشروع في مهام إضافية واستفسارات لحتى نتأكد انه فهمنا

- نبلش الرحلة بإطار العمل ورح نتعلم ال react and vue ونبني فيهن مشاريع وندخل بالأساسيات متل 
components & routing & state management

الإشتراك مااانه كورس، الإشتراك هو بيئة عم تتعلم فيها مع ناس بنفس شغفك ورح يكون في اجتماعات دورية.

كيف منبدأ ؟
لما بيتم قبولك رح توصلك دعوة للمجتمع ورح نعمل اجتماع 15د نحكي فيه شو الآلية يلي رح نتبعها والأهداف.

وتاني يوم منعمل اجتماع لنتعرف ع كل شخص شو متعلم ومن وين رح يبدأ لنحطله الخطة المخصصة.

بالأسبوع التاني رح يتم تسجيل الأسماء لشحن نسخة شغوف ولكن النسخة رح تكون مرجع لبعدين، إنما بالإشتراك رح نكون ماشيين عالمصادر يلي منبعتها مباشرةً.
"""

TEXT_USERNAME_WARNING = """ياريت نحط معرف تلغرام كرمال اقدر اتواصل معك، وطبعاً المعرف غير الإسم انتبه وفوت غيرها من الإعدادات وبعدها ارجع اعمل start للبوت"""

TEXT_STEP2 = """مدة الإشتراك لهالمتابعة رح تكون شهرين.

⚠️ والإشتراك للناس يلي بدها تستثمر هالشهرين من وقتها مو للناس يلي داخلة تجرب حالها.

💴 والتكلفة 4 قمحات من العملة الجديدة 🌾

بأول شهر وعند القبول يتم تسديد قيمة 3 قمحات، وبالشهر التاني يتم تسديد الكمالة.

طيب ليش ما ندفعها كلها سوا وخلص ؟

- ممكن اكتشف ناس مقصرين او ماعندن همة كافية، ف بعتذر منهن من الشهر التاني وهيك انا بيرتاح ضميري انه لسه مو دافعين

- ممكن شخص مستواه منيح ولكن مقصر بالمشاريع ف كان كافي اله شهر واحد، وحرام اضحك عليه واخليه يدفع لشهرين.

- ممكن صار معك ظرف ومابدك تكمل او طلعت متخاذل، ساعتها ما بتحس حالك تخورفت ودفعت شهرين لقدام.

بالمختصر انا ما هدفي تجاري، هدفي انه انا ارتاح بالمتابعة واعرف الناس ملتزمة وانتو كمان مرتاحين ومبسوطين من النتائج يلي عم تطلع بإذن الله.

هلق اذا انت متأكد مليار بالمية انه رح تكمل ف اكبس على تأكيد ورح يوصلك دعوة خلال يومين
"""

KB_CONTINUE = InlineKeyboardMarkup(
    [[InlineKeyboardButton("متابعة", callback_data="continue")]]
)

KB_CONFIRM_CANCEL = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("تأكيد ✅", callback_data="confirm")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel")],
    ]
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else f"ID: {user.id}"

    await context.bot.send_message(
        ASK_CHAT_ID,
        f"{user.full_name}\n{username}"
    )

    if not user.username:
        await update.message.reply_text(TEXT_USERNAME_WARNING)
        return

    userState[user.id] = {"step": "start"}

    await update.message.reply_text(
        TEXT_START,
        reply_markup=KB_CONTINUE
    )


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user = q.from_user
    cid = user.id
    data = q.data

    if data == "continue":
        userState[cid] = {"step": "confirm"}
        await q.edit_message_text(TEXT_STEP2, reply_markup=KB_CONFIRM_CANCEL)

    elif data == "confirm":
        username = f"@{user.username}" if user.username else f"ID: {user.id}"

        await context.bot.send_message(
            ORDERS_CHAT_ID,
            f"""اشتراك جديد:
الاسم: {user.full_name}
المعرف: {username}"""
        )

        await q.edit_message_text("تم تسجيل طلبك ✅")
        userState.pop(cid, None)

    elif data == "cancel":
        userState.pop(cid, None)
        await q.edit_message_text("تم الإلغاء ❌")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))

    app.run_polling()


if __name__ == "__main__":
    main()