from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


TOKEN = "8366088074:AAGWJTxHIWXo08Pdn9h-HKBZuc5URzNx_Fg"
ADMIN_CHAT_ID = "895332862"
ORDERS_CHAT_ID = "-1002993388534"
ASK_CHAT_ID = "-1003196454615"

userAsks = {}
userOrders = {}

mainMenu = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🟠 نسخة فرونت 🟠", callback_data="front")],
        [InlineKeyboardButton("🟢 نسخة الباك 🟢", callback_data="back")],
        [InlineKeyboardButton("🟣 نسخة التأسيس 🟣", callback_data="foundation")],
        [InlineKeyboardButton("⁉️ محتار وعندك استفسار ⁉️", callback_data="ask")],
    ]
)
versionsInfo = {
    "front": """فرونت إيند شغوف ✨

📗 هالنسخة مخصصة لتعلم أساسيات المجال بخطوات واضحة ومنظمة، من HTML، CSS مع 3 تطبيقات عملية

📗 وبتبدأ Javascript مع كورس الزيرو مُقسّم لفصلين لحتى ما تحس بملل من الكورس.

📗 ولتثبت المعلومات رح تشتغل على تطبيقين عمليين مع مهام إضافية بعد كل تطبيق لحتى تتخطى حدود الكورسات 🔥

📗 وتكملة الرحلة مع React or Vue على حسب رغبتك، لكَ حُرية الإختيار، مع تطبيقين عمليين ومهام إضافية كمان.

⛳️ كل فصل مجهز بطريقة عملية:

🔸 أمثلة تطبيقية مباشرة.
🔸 أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
🔸 مساحة لتدوين ملاحظاتك أثناء التعلم.
🔸 وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
""",
    "back": """باك إيند شغوف ✨

📗 كورس PHP على فصلين حتى تتعلم الأساسيات بدون ملل وبشكل تدريجي في حال كنت شايف الكورس طويل.

📗 كورس SQL لتتعلم التعامل مع قواعد البيانات، كتابة الاستعلامات، وإدارة البيانات يلي هي أساس الباك إيند طبعاً.

📗 وبتكمل الرحلة مع كورسين كاملين في Laravel لتبني تطبيقات قوية وحديثة، مع كل المهارات اللي تحتاجها كمطوّر باك إيند. 🔥

⛳️ كل فصل مجهز بطريقة عملية:

🔸 أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
🔸 مساحة لتدوين ملاحظاتك أثناء التعلم.
🔸 وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
""",
    "foundation": """الأساسيات مع شغوف ✨

هالنسخة مصممة لتأسيسك في البرمجة بشكل قبل ما تنتقل لأي مجال ومالك بحاجة معرفة مسبقة بالبرمجة ابداً، رح تبدأ ببناء أساس قوي إن شاء الله.

🟥 عندك خيارين، إما بايثون او C++

📗 كورس ++C على فصلين حتى تتعلم الأساسيات بدون ملل وبشكل تدريجي في حال كنت شايف الكورس طويل.

📗 كورس OOP لتجهّز حالك لمفاهيم مادة برمجة 2، وتكون عم تكمّل الأساسيات يلي تعلمتها بال ++C

📗 كورس بايثون حتى تتعلم الأساسيات كمان.

📗 فصل التطبيقات الع 
ملية: تطبيقين عمليين مع مهام إضافية بعد ماتخلص كرمال تختبر حالك وتتخطى حدود الكورس

⛳️ كل فصل مجهز بطريقة عملية:

🔸 أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
🔸 مساحة لتدوين ملاحظاتك أثناء التعلم.
🔸 وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
""",
    "start": """مرحباً بك في شغوف ✨
    شغوف هو صديق رحلتك البرمجية، مابهم المستوى سواء من الصفر او مبلش من قبل، كلشي رح يكون بخطوات واضحة وبسيطة. هدفه يسهّل عليك الطريق ويخلّي التعلم ممتع بعيد عن العشوائية.
    🎯 ليش شغوف؟
    التشتت دوماً ياصديقي أكبر عدو للمبتدئين! رح تلاقي كل شيء محتاجه بمكان واحد: مسار تعليمي مرتب، أدوات لإدارة وقتك، وتحفيز يخلّيك تكمل بدون ما توقف إن شاء الله.
    بكل فصل رح تلاقي:
    🔸 قسم قبل أن تبدأ وبعد أن تنتهي:
    مقدمة واضحة تعملك تهيئة نفسية تشرحلك ليش هالموضوع كيف رح يفيدك.
    🔸 قائمة (To-Do) خاصة بالدروس:
    كل العناوين يلي مرّيت عليها في الفيديوهات بتكون مرتبة، حتى تتابع شو خلصت وشو باقي.
    🔸 مساحة حرة لكتابة ملاحظاتك:
    أفكارك، ملاحظاتك، أي فكرة تمر عليك… مكان واحد يجمع كل شي.
    🔸 مهامك اليومية الشخصية:
    قسم مخصص لتكتب جدولك اليومي وتحدد أولوياتك بطريقتك.
    بإمكانك تشوف صور النسخ من القناة:
    https://t.me/baraa_developer
    أو تلغرام التواصل في حال مالقيت الخدمة المناسبة بالبوت:
    @shagh1
    🚀 شغوف بانتظارك ليصنع معك تجربة جديدة، اختر النسخة الخاصة فيك وخلينا نبدأ..
    """,
    "ask": """محتار بأي مجال تبلش وبدك استشارة لحتى تتطمن إنك قررت صح ؟
فيك تترك سؤالك برسالة على المعرف @shagh1 ✉️
ورح اتواصل معك وأجاوب بأسرع وقت إن شاء الله..

فضلاً خلي سؤالك مختصر وواضح برسالة واحدة حتى أقدر ساعدك بأفضل شكل عزيزي الشغوف ✨

""",
    "orderInfo": """شكراً إنك وصلت لهالمرحلة 🎗

هالمرحلة قبل الأخيرة قبل ما تشوف السعر النهائي وتختار إذا بتكمل أو بتلغي الطلب 👇

🟥 إذا كنت بحلب:
🔸 الإستلام رح يكون بمكتبة دعبول بأدونيس بعد ماتسجل اسمك بالطلب

🟥 إذا كنت بغير محافظة:
🔸 الشحن عبر القدموس
ورح أتواصل معك للدفع عن طريق شام كاش، طريقة سهلة حتى لو أول مرة تستخدمها 👀

اكتبلي معلوماتك بهالشكل لنكمل آخر خطوة ومعرفة السعر 💵:

- الاسم الثلاثي
- المحافظة
- الرقم
- اذا بحلب اكتبلي أدونيس (أو أقرب منطقة للقدموس إذا خارج حلب)

مثلاً:
براء صلاح نيال
حلب
09393939393
أدونيس

⚪️ أو ⚪️

براء صلاح نيال
دمشق
09393939393
قدموس أشرفية صحنايا

———————————————————————

ولا تخاف، فيك تلغي الطلب أو تثبّته بالمرحلة الجاي… عليك الأمان 🤝

اكتبلي 👇
""",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(versionsInfo["start"], reply_markup=mainMenu)
    


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data
    text = ""
    keyboard = None

    if data in ["front", "back", "foundation"]:
        text = versionsInfo[data]
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "اطلب هالنسخة ✅", callback_data=f"order_{data}"
                    )
                ],
                [InlineKeyboardButton("رجوع للقائمة ⭕️", callback_data="menu")],
            ]
        )
    elif data == "ask":
        await query.edit_message_text(
            versionsInfo["ask"],
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("رجوع للقائمة", callback_data="menu")]]
            ),
        )
        return
    elif data == "menu":
        await query.edit_message_text(versionsInfo["start"], reply_markup=mainMenu)
        return
    elif data.startswith("order_"):
        version = data.replace("order_", "")
        userOrders[chat_id] = {"version": version, "step": "awaiting_info"}
        await query.edit_message_text(versionsInfo["orderInfo"])
        return
    elif data == "confirm_order":
        order = userOrders.get(chat_id)
        if not order:
            return

        userOrders[chat_id]["step"] = "awaiting_contact"

        await query.edit_message_text(
            " شكراً لتأكيد الطلب! لطفاً شارك رقمك الشخصي عبر زر مشاركة الرقم أدناه لحتى أقدر أتواصل معك وقت التسليم أو الشحن وبوعدك مارح اهكرك ولا فيها خطورة ع حياتك 🤣"
        )

        contact_button = KeyboardButton("📞 شارك رقمي", request_contact=True)
        reply_markup = ReplyKeyboardMarkup(
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True
        )

        await context.bot.send_message(
            chat_id,
            "اضغط على الزر لمشاركة رقمك الشخصي:",
            reply_markup=reply_markup,
        )

    elif data == "cancel_order":
        await query.edit_message_text(
            "❌ تم إلغاء الطلب. إذا حاب تشاركنا السبب تواصل مع @shagh1"
        )
        username = (
            f"@{query.from_user.username}"
            if query.from_user.username
            else f"ID: {chat_id}"
        )
        await context.bot.send_message(
            ASK_CHAT_ID, f"⚠️ User {username} canceled the order."
        )
        if chat_id in userOrders:
            del userOrders[chat_id]
        return

    if text:
        await query.edit_message_text(text, reply_markup=keyboard)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in userAsks:
        del userAsks[chat_id]
        username = (
            f"@{update.message.from_user.username}"
            if update.message.from_user.username
            else f"ID: {chat_id}"
        )
        await update.message.reply_text("✅ تم إرسال سؤالك")
        await context.bot.send_message(
            ASK_CHAT_ID, f"📩 User: {username}\n\nQuestion:\n{update.message.text}"
        )
        return

    if chat_id in userOrders and userOrders[chat_id]["step"] == "awaiting_contact":
        if update.message.contact:  # user shared contact
            contact_number = update.message.contact.phone_number
            if not contact_number.startswith("+"):
                contact_number = f"+{contact_number}"

            username = (
                f"@{update.message.from_user.username}"
                if update.message.from_user.username
                else f"ID: {chat_id}"
            )
            order = userOrders[chat_id]

            await context.bot.send_message(
                ORDERS_CHAT_ID,
                f"📢 New Order Confirmed!\n\nنسخة: {order['version']}\n"
                f"المحافظة: {order['governorate']}\n"
                f"الاسم: {order['name']}\n"
                f"الرقم المدخل: {order['number']}\n"
                f"الموقع: {order['location']}\n"
                f"السعر بعد الحسم: {order['price']} ألف\n"
                f"رقم للتواصل: {contact_number} ({username})",
            )

            await update.message.reply_text(
                "📦 رح يتم توصية نسخة للطباعة ورح أتواصل معك بس تجهز. إذا كانت شحن، رح ابعتلك وصل الشحن تلقائياً بس تنشحن. أما إذا التسليم بحلب، فبكون بالتنسيق معي مباشرة. وأي سؤال، شغوف دايماً موجود ✨"
            )
            del userOrders[chat_id]
        else:
            await update.message.reply_text(
                "❌ الرجاء مشاركة رقمك الشخصي عبر الزر المخصص لذلك."
            )
        return

    if chat_id in userOrders and userOrders[chat_id]["step"] == "awaiting_info":
        lines = update.message.text.split("\n")
        if len(lines) < 4:
            await update.message.reply_text(
                "الرجاء إدخال البيانات بهالشكل وبرسالة واحدة:\n الاسم\nالمحافظة\nالرقم\nالموقع"
            )
            return

        name, governorate, number, location = (
            lines[0].strip(),
            lines[1].strip(),
            lines[2].strip(),
            lines[3].strip(),
        )
        version = userOrders[chat_id]["version"]

        discount_front_price = 0
        front_main_price = 0
        others_main_price = 0
        discount_others_price = 0

        user_price = (
            discount_front_price if version == "front" else discount_others_price
        )

        userOrders[chat_id] = {
            "version": version,
            "name": name,
            "governorate": governorate,
            "number": number,
            "location": location,
            "price": user_price,
        }

    await update.message.reply_text(
        f"""نسخة: {version}
المحافظة: {governorate}
الاسم: {name}
الرقم: {number}
الموقع: {location}

السعر الأساسي {"{0}$".format(front_main_price) if version == "front" else "{0}$".format(others_main_price)}
وبحسم هالأسبوع رح يصير السعر: {"{0} ألف".format(discount_front_price) if version == "front" else "{0} ألف".format(discount_others_price)}

ويتضمن ميدلية بورتكليه ذِكرى من شغوف 💫.

فضلاً إذا ماكنت متأكد إنك رح تستلم النسخة ف لاتكمَل الطلب، لأن عدد النسخ محدود ف اترك فرصة لغيرك ولاتضرني بوصولنا لمرحلة التسليم وماتستلم،
تأكيد مرة أخيرة تمام؟""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "رح استلم وما ضيّع تعبك 😁", callback_data="confirm_order"
                    )
                ],
                [InlineKeyboardButton("إلغاء الطلب 👀", callback_data="cancel_order")],
            ]
        ),
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND | filters.CONTACT, handle_message
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
