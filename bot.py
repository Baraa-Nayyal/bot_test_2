import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8366088074:AAG-rZRAQJzLkw6R6nTs8tnFTMNezPAhpL0"
ADMIN_CHAT_ID = "895332862"
ORDERS_CHAT_ID = "-4873158541"
ASK_CHAT_ID = "-4810733126"

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

أمثلة تطبيقية مباشرة.
أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
مساحة لتدوين ملاحظاتك أثناء التعلم.
وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
""",
    "back": """باك إيند شغوف ✨

📗 كورس PHP على فصلين حتى تتعلم الأساسيات بدون ملل وبشكل تدريجي في حال كنت شايف الكورس طويل.

📗 كورس SQL لتتعلم التعامل مع قواعد البيانات، كتابة الاستعلامات، وإدارة البيانات يلي هي أساس الباك إيند طبعاً.

📗 وبتكمل الرحلة مع كورسين كاملين في Laravel لتبني تطبيقات قوية وحديثة، مع كل المهارات اللي تحتاجها كمطوّر باك إيند. 🔥

⛳️ كل فصل مجهز بطريقة عملية:

أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
مساحة لتدوين ملاحظاتك أثناء التعلم.
وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
""",
    "foundation": """الأساسيات مع شغوف ✨

هالنسخة مصممة لتأسيسك في البرمجة بشكل قبل ما تنتقل لأي مجال ومالك بحاجة معرفة مسبقة بالبرمجة ابداً، رح تبدأ ببناء أساس قوي إن شاء الله.

🟥 عندك خيارين، إما بايثون او C++

📗 كورس ++C على فصلين حتى تتعلم الأساسيات بدون ملل وبشكل تدريجي في حال كنت شايف الكورس طويل.

📗 كورس OOP لتجهّز حالك لمفاهيم مادة برمجة 2، وتكون عم تكمّل الأساسيات يلي تعلمتها بال ++C

📗 كورس بايثون حتى تتعلم الأساسيات كمان.

📗 فصل التطبيقات العملية: تطبيقين عمليين مع مهام إضافية بعد ماتخلص كرمال تختبر حالك وتتخطى حدود الكورس

⛳️ كل فصل مجهز بطريقة عملية:

أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
مساحة لتدوين ملاحظاتك أثناء التعلم.
وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
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
@shaghoof1


🚀 شغوف بانتظارك ليصنع معك تجربة جديدة، اختر النسخة الخاصة فيك وخلينا نبدأ..
""",
    "ask": """محتار بأي مجال تبلش وبدك استشارة لحتى تتطمن إنك قررت صح ؟
فيك تترك سؤالك برسالة ✉️
تأكد إنك مأظهر معرفك التلغرام ورح اتواصل معك وأجاوب خلال ساعات قليلة إن شاء الله..

فضلاً خلي سؤالك مختصر وواضح برسالة واحدة حصراً حتى أقدر ساعدك بأفضل شكل عزيزي الشغوف ✨

اكتبلي 👇
""",
    "orderInfo": """شكراً إنك وصلت لهالمرحلة 🎗

🔸فيك  تستلم النسخة بشكل مجاني بمنطقة الأكرمية أو حلب الجديدة شمالي

🔹 غير هيك في خيار دليفري لبيتك بأسرع وقت بتكلفة مابتتجاوز 15 ألف على حسب منطقة بيتك


اكتبلي معلوماتك بهالشكل صديقي لنوصل لآخر مرحلة بالطلب:

- الاسم
- الرقم
- المنطقة يلي بتحب تستلم منها: أكرمية، حلب الجديدة، دليفري

مثلاً:
براء نيال
0988888888
أكرمية

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
        userAsks[chat_id] = True
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
        await query.edit_message_text("✅ تم تأكيد الطلب، رح أتواصل معك قريباً")
        username = (
            f"@{query.from_user.username}"
            if query.from_user.username
            else f"ID: {chat_id}"
        )
        await context.bot.send_message(
            ORDERS_CHAT_ID,
            f"📢 New Order Confirmed!\n\nنسخة: {order['version']}\n"
            f"الاسم: {order['name']}\nالرقم: {order['number']}\n"
            f"الموقع: {order['location']}\nالمستخدم: {username}",
        )
        del userOrders[chat_id]
        return
    elif data == "cancel_order":
        await query.edit_message_text(
            "❌ تم إلغاء الطلب. إذا حاب تشاركنا السبب تواصل مع @shaghoof1"
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

    if chat_id in userOrders and userOrders[chat_id]["step"] == "awaiting_info":
        lines = update.message.text.split("\n")
        if len(lines) < 3:
            await update.message.reply_text(
                "الرجاء إدخال البيانات: الاسم\nالرقم\nالموقع"
            )
            return

        name, number, location = lines[0].strip(), lines[1].strip(), lines[2].strip()
        version = userOrders[chat_id]["version"]

        front_price = 75
        front_main_price = 15
        others_main_price = 12
        others_price = 60

        userOrders[chat_id] = {
            "version": version,
            "name": name,
            "number": number,
            "location": location,
        }

    await update.message.reply_text(
        f"""نسخة: {version}
الاسم: {name}
الرقم: {number}
الموقع: {location}

السعر الأساسي {"{0}$".format(front_main_price) if version == "front" else "{0}$".format(others_main_price)}
وبحسم للنسخ الأولى رح يصير السعر: {"{0} ألف".format(front_price) if version == "front" else "{0} ألف".format(others_price)}

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
