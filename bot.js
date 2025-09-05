const TelegramBot = require("node-telegram-bot-api");

require("dotenv").config();

const TOKEN = process.env.BOT_TOKEN;
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID;
const ORDERS_CHAT_ID = process.env.ORDERS_CHAT_ID;
const ASK_CHAT_ID = process.env.ASK_CHAT_ID;

const bot = new TelegramBot(TOKEN, { polling: true });

const mainMenu = {
  reply_markup: {
    inline_keyboard: [
      [{ text: "🟠 نسخة sssss 🟠", callback_data: "front" }],
      [{ text: "🟢 نسخة الباك 🟢", callback_data: "back" }],
      [{ text: "🟣 نسخة التأسيس 🟣", callback_data: "foundation" }],
      [{ text: "⁉️ محتار وعندك استفسار ⁉️", callback_data: "ask" }],
    ],
  },
};

const userAsks = {};

const versionsInfo = {
  front: `فرونت إيند شغوف ✨

📗 هالنسخة مخصصة لتعلم أساسيات المجال بخطوات واضحة ومنظمة، من HTML، CSS مع 3 تطبيقات عملية

📗 وبتبدأ Javascript مع كورس الزيرو مُقسّم لفصلين لحتى ما تحس بملل من الكورس.

📗 ولتثبت المعلومات رح تشتغل على تطبيقين عمليين مع مهام إضافية بعد كل تطبيق لحتى تتخطى حدود الكورسات 🔥

📗 وتكملة الرحلة مع React or Vue على حسب رغبتك، لكَ حُرية الإختيار، مع تطبيقين عمليين ومهام إضافية كمان.

⛳️ كل فصل مجهز بطريقة عملية:

أمثلة تطبيقية مباشرة.
أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
مساحة لتدوين ملاحظاتك أثناء التعلم.
وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
`,

  back: `باك إيند شغوف ✨

📗 كورس PHP على فصلين حتى تتعلم الأساسيات بدون ملل وبشكل تدريجي في حال كنت شايف الكورس طويل.

📗 كورس SQL لتتعلم التعامل مع قواعد البيانات، كتابة الاستعلامات، وإدارة البيانات يلي هي أساس الباك إيند طبعاً.

📗 وبتكمل الرحلة مع كورسين كاملين في Laravel لتبني تطبيقات قوية وحديثة، مع كل المهارات اللي تحتاجها كمطوّر باك إند. 🔥

⛳️ كل فصل مجهز بطريقة عملية:

أسئلة قصيرة بعد كل فصل لتتأكد من فهمك.
مساحة لتدوين ملاحظاتك أثناء التعلم.
وطبعاً To-Do لكل الدروس لترتيب تقدمك بسهولة.
`,

  foundation: `الأساسيات مع شغوف ✨

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
`,

  start: `
  مرحباً بك في شغوف ✨
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


🚀 شغوف بانتظارك ليصنع معك تجربة جديدة، اختر النسخة الخاصة فيك وخلينا نبدأ..
  `,

  ask: `محتار بأي مجال تبلش وبدك استشارة لحتى تتطمن إنك قررت صح ؟
فيك تترك سؤالك برسالة ✉️
تأكد إنك مأظهر معرفك التلغرام ورح اتواصل معك وأجاوب خلال ساعات قليلة إن شاء الله..

فضلاً خلي سؤالك مختصر وواضح برسالة واحدة حصراً حتى أقدر ساعدك بأفضل شكل عزيزي الشغوف ✨

اكتبلي 👇
`,

  orderInfo: `
  شكراً إنك وصلت لهالمرحلة 🎗

اكتبلي معلوماتك بهالشكل صديقي:

- الاسم
- الرقم
- المنطقة يلي بتحب تستلم منها: أكرمية، حلب الجديدة، توصيل دليفري

مثلاً:
براء نيال
0988888888
أكرمية

اكتبلي 👇
`,
};

const userOrders = {};

bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;

  bot
    .sendMessage(chatId, versionsInfo.start, mainMenu)
    .catch((err) => console.error("Send Message Error:", err));
});
// -4873158541

bot.on("callback_query", (query) => {
  const chatId = query.message.chat.id;
  let text = "";
  let keyboard = [];

  if (["front", "back", "foundation"].includes(query.data)) {
    text = versionsInfo[query.data];
    keyboard = [
      [{ text: "اطلب هالنسخة ✅", callback_data: `order_${query.data}` }],
      [{ text: "رجوع للقائمة ⭕️", callback_data: "menu" }],
    ];
  } else if (query.data === "ask") {
    userAsks[chatId] = true; // ℹ mark user as waiting to send a question

    text = versionsInfo.ask;
    keyboard = [[{ text: "رجوع للقائمة", callback_data: "menu" }]];

    bot.editMessageText(versionsInfo.ask, {
      chat_id: chatId,
      message_id: query.message.message_id,
    });
    return;
  } else if (query.data === "menu") {
    bot.editMessageText(versionsInfo.start, {
      chat_id: chatId,
      message_id: query.message.message_id,
      reply_markup: mainMenu.reply_markup,
    });
    return;
  } else if (query.data.startsWith("order_")) {
    const version = query.data.replace("order_", "");

    userOrders[chatId] = { version, step: "awaiting_info" };

    bot.editMessageText(versionsInfo.orderInfo, {
      chat_id: chatId,
      message_id: query.message.message_id,
    });
    return;
  }
  // Order step 1: ask info
  else if (query.data.startsWith("order_")) {
    const version = query.data.replace("order_", "");
    userOrders[chatId] = { version, step: "awaiting_info" };
    bot.editMessageText(versionsInfo.orderInfo, {
      chat_id: chatId,
      message_id: query.message.message_id,
    });
    return;
  }

  // Order step 2: continue / back
  else if (query.data === "continue_order") {
    const order = userOrders[chatId];
    if (!order) return;

    userOrders[chatId].step = "awaiting_final_confirmation";

    bot.editMessageText(
      `عند الضغط على "تأكيد"، رح يتم طلب طباعة نسخة خاصة فيك ورح اتواصل معك بأقرب وقت ممكن إن شاء الله.\n\n` +
        `نسخة: ${order.version}\n` +
        `الاسم: ${order.name}\n` +
        `الرقم: ${order.number}\n` +
        `الموقع: ${order.location}\n` +
        `السعر: ${order.version === "front" ? "95 ألف" : "75 ألف"}\n\n` +
        `ويتضمن ميدلية بورتكليه ذِكرى من شغوف.\n\n` +
        `فضلاً إذا ماكنت متأكد إنك رح تستلم النسخة ف لاتكمَل الطلب، لأن عدد النسخ محدود ف اترك فرصة لغيرك ولاتضرني بوصولنا لمرحلة التسليم وماتستلم؟`,
      {
        chat_id: chatId,
        message_id: query.message.message_id,
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: "رح استلم وما ضيّع تعبك 😁 ",
                callback_data: "confirm_order",
              },
            ],
            [{ text: "إلغاء الطلب 👀 ", callback_data: "cancel_order" }],
          ],
        },
      }
    );
    return;
  } else if (query.data === "back_order") {
    const order = userOrders[chatId];
    if (!order) return;

    userOrders[chatId].step = "awaiting_info";

    bot.editMessageText(versionsInfo.orderInfo, {
      chat_id: chatId,
      message_id: query.message.message_id,
    });
    return;
  }
  // Step 3: confirm / cancel
  else if (query.data === "confirm_order") {
    const order = userOrders[chatId];
    if (!order) return;

    bot.editMessageText(
      "✅ تم تأكيد الطلب، وشكراً لأن كنت جزء من رحلة شغوف،\n رح أتواصل معك بأقرب فرصة",
      {
        chat_id: chatId,
        message_id: query.message.message_id,
      }
    );

    const username = query.message.from.username
      ? `@${query.message.from.username}`
      : `ID: ${chatId}`;

    bot.sendMessage(
      ORDERS_CHAT_ID,
      `📢 New Order Confirmed!\n\nنسخة: ${order.version}\nالاسم: ${order.name}\nالرقم: ${order.number}\nالموقع: ${order.location}\nالمستخدم: ${username}`
    );

    delete userOrders[chatId];
    return;
  } else if (query.data === "cancel_order") {
    const order = userOrders[chatId];
    if (!order) return;

    bot.editMessageText(
      `
❌ تم إلغاء الطلب. إذا حاب تشاركنا السبب أو تحتاج مساعدة تواصل مع @shaghoof1، و شغوف جاهز يدعمك لتبدأ برحلتك الخاصة ✨      `,
      {
        chat_id: chatId,
        message_id: query.message.message_id,
      }
    );

    const username = query.from.username
      ? `@${query.from.username}`
      : `ID: ${chatId}`;

    bot.sendMessage(ASK_CHAT_ID, `⚠️ User ${username} canceled the order.`);

    delete userOrders[chatId];
    return;
  } else {
    bot.editMessageText(text, {
      chat_id: chatId,
      message_id: query.message.message_id,
      reply_markup: { inline_keyboard: keyboard },
    });
  }

  bot.editMessageText(text, {
    chat_id: chatId,
    message_id: query.message.message_id,
    reply_markup: { inline_keyboard: keyboard },
  });
});

const locations = ["أكرمية", "حلب الجديدة", "دليفري"];

bot.on("message", (msg) => {
  const chatId = msg.chat.id;

  if (userAsks[chatId]) {
    delete userAsks[chatId];

    const username = msg.from.username
      ? `@${msg.from.username}`
      : `ID: ${chatId}`;
    bot.sendMessage(chatId, "✅ تم إرسال سؤالك، رح اتواصل معك بأسرع وقت");

    bot.sendMessage(
      ASK_CHAT_ID,
      `📩 User Telegram: ${username}\n\nQuestion:\n${msg.text}`
    );
    return;
  }

  if (userOrders[chatId] && userOrders[chatId].step === "awaiting_info") {
    const userInput = msg.text.split("\n");
    if (userInput.length < 3) {
      bot.sendMessage(
        chatId,
        "الرجاء إدخال البيانات بالشكل المطلوب:\nالاسم\nالرقم\nالموقع"
      );
      return;
    }

    const name = userInput[0].trim();
    const number = userInput[1].trim();
    const location = userInput[2].trim();
    const version = userOrders[chatId].version;

    const numberRegex = /^09\d{8}$/;
    // if (!numberRegex.test(number)) {
    //   bot.sendMessage(
    //     chatId,
    //     "❌ الرقم غير صحيح. لازم يبدأ بـ 09 ويكون 10 أرقام."
    //   );
    //   return;
    // }

    // if (!locations.includes(location)) {
    //   bot.sendMessage(
    //     chatId,
    //     `❌ الموقع غير صحيح. لازم تختار من: ${locations.join(", ")}`
    //   );
    //   return;
    // }

    // Save data and move to next step
    userOrders[chatId] = {
      version,
      name,
      number,
      location,
      step: "awaiting_final_confirmation",
    };

    bot.sendMessage(
      chatId,
      `عند الضغط على "تأكيد"، رح يتم طلب طباعة نسخة خاصة فيك ورح اتواصل معك بأقرب وقت ممكن إن شاء الله كرمال التسليم.\n\n` +
        `نسخة: ${version}\n` +
        `الاسم: ${name}\n` +
        `الرقم: ${number}\n` +
        `الموقع: ${location}\n\n` +
        `رح يكون سعر النسخة ${version === "front" ? "95 ألف" : "75 ألف"}\n` +
        `ويتضمن ميدلية بورتكليه ذِكرى من شغوف 💫.\n\n` +
        `فضلاً إذا ماكنت متأكد إنك رح تستلم النسخة ف لاتكمَل الطلب، لأن عدد النسخ محدود ف اترك فرصة لغيرك ولاتضرني بوصولنا لمرحلة التسليم وماتستلم،\n تأكيد مرة أخيرة تمام؟`,
      {
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: "رح استلم وما ضيّع تعبك 😁 ",
                callback_data: "confirm_order",
              },
            ],
            [{ text: "إلغاء الطلب 👀 ", callback_data: "cancel_order" }],
          ],
        },
      }
    );
  }

  // if (userOrders[chatId] && userOrders[chatId].step === "awaiting_info") {
  //   const userInput = msg.text.split("\n");
  //   if (userInput.length < 3) {
  //     bot.sendMessage(
  //       chatId,
  //       "الرجاء إدخال البيانات بالشكل المطلوب:\nالاسم\nالرقم\nالموقع"
  //     );
  //     return;
  //   }

  //   const name = userInput[0].trim();
  //   const number = userInput[1].trim();
  //   const location = userInput[2].trim();
  //   const version = userOrders[chatId].version;

  //   // Validate number
  //   const numberRegex = /^09\d{8}$/; // starts with 09 and total 10 digits

  //   console.log(number);
  //   if (!numberRegex.test(number)) {
  //     bot.sendMessage(
  //       chatId,
  //       "❌ الرقم غير صحيح. لازم يبدأ بـ 09 ويكون 10 أرقام."
  //     );
  //     return;
  //   }

  //   // Validate location
  //   if (!locations.includes(location)) {
  //     bot.sendMessage(
  //       chatId,
  //       `❌ الموقع غير صحيح. لازم تختار من: ${locations.join(", ")}`
  //     );
  //     return;
  //   }

  //   delete userOrders[chatId];

  //   bot.sendMessage(chatId, "✅ تم تسجيل طلبك، رح نتواصل معك فوراً");

  //   const username = msg.from.username
  //     ? `@${msg.from.username}`
  //     : `ID: ${chatId}`;
  //   bot.sendMessage(
  //     ORDERS_CHAT_ID,
  //     `📢 New Order Submitted!\n\nنسخة: ${version}\nالاسم: ${name}\nالرقم: ${number}\nالموقع: ${location}\nالمستخدم: ${username}`
  //   );
  // }
});

//   if (query.data === "front") {
//   bot.sendPhoto(chatId, "C:/Users/BRO/Desktop/test/f.jpg").then(() => {
//     bot.sendMessage(chatId, "شرح نسخة الفرونت...\n\n", {
//       reply_markup: {
//         inline_keyboard: [
//           [{ text: "اطلب هالنسخة", callback_data: "order_front" }],
//           [{ text: "شوف باقي النسخ", callback_data: "menu" }],
//         ],
//       },
//     });
//   });
// }

// if (query.data === "front") {
//   text = "شرح نسخة الفرونت...\n\n";
//   keyboard = [
//     [{ text: "اطلب هالنسخة", callback_data: "order_front" }],
//     [{ text: "شوف باقي النسخ", callback_data: "menu" }],
//   ];
// } else if (query.data === "back") {
//   text = "شرح نسخة الباك...\n\n";
//   keyboard = [
//     [{ text: "اطلب هالنسخة", callback_data: "order_back" }],
//     [{ text: "شوف باقي النسخ", callback_data: "menu" }],
//   ];
// } else if (query.data === "foundation") {
//   text = "شرح نسخة التأسيس...\n\n";
//   keyboard = [
//     [{ text: "اطلب هالنسخة", callback_data: "order_foundation" }],
//     [{ text: "شوف باقي النسخ", callback_data: "menu" }],
//   ];
// } else if (query.data === "ask") {
//   text = "إذا محتار فيك تراسلني هون: @YourUsername";
//   keyboard = [[{ text: "رجوع للقائمة", callback_data: "menu" }]];
// } else if (query.data === "menu") {
//   bot.editMessageText(
//     "أهلاً بك! هاد البوت الخاص بطلب نسخ شغوف.\nاختر النسخة يلي بتناسبك:",
//     {
//       chat_id: chatId,
//       message_id: query.message.message_id,
//       reply_markup: mainMenu.reply_markup,
//     }
//   );
//   return;
// } else if (query.data.startsWith("order_")) {
//   const version = query.data.replace("order_", "");

//   userOrders[chatId] = { version, step: "awaiting_info" };

//   bot.editMessageText("رجاءً اكتب بياناتك بهالشكل:\n\nالاسم\nالرقم\nالموقع", {
//     chat_id: chatId,
//     message_id: query.message.message_id,
//   });
//   return;
// }
