import os
import sqlite3
from datetime import date, datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

DB_PATH = "bot.db"

ADMIN_ID = 7861055850
TOKEN = "8258955051:AAGyadE7trmPI93VJtpAPS4GbboO4AwSVTo"


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            active INTEGER DEFAULT 1,
            registered_at TEXT,
            points INTEGER DEFAULT 0
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_done (
            user_id INTEGER NOT NULL,
            done_date TEXT NOT NULL,
            message TEXT NOT NULL,
            done_time TEXT NOT NULL,
            done_time_iso TEXT NOT NULL,
            PRIMARY KEY (user_id, done_date)
        )
        """
    )

    conn.commit()
    conn.close()


def upsert_user(user_id: int, username: str, name: str):
    now_iso = datetime.now().isoformat(timespec="seconds")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cur.fetchone() is not None

    if not exists:
        cur.execute(
            "INSERT INTO users (user_id, username, name, active, registered_at) VALUES (?, ?, ?, 1, ?)",
            (user_id, username, name, now_iso),
        )
    else:
        cur.execute(
            "UPDATE users SET username = ?, name = ?, active = 1 WHERE user_id = ?",
            (username, name, user_id),
        )

    conn.commit()
    conn.close()


def get_user_active(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT active FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return bool(row and row[0] == 1)


def remove_user_by_username(username: str) -> bool:
    username = username.lstrip("@").strip()
    if not username:
        return False

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE username = ? AND active = 1",
        (username,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return False

    user_id = row[0]
    cur.execute("UPDATE users SET active = 0 WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM daily_done WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()
    return True


def mention(user_id: int, name: str) -> str:
    safe = (name or "User").replace("[", "(").replace("]", ")")
    return f"[{safe}](tg://user?id={user_id})"


async def send_in_topic(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="Markdown",
        message_thread_id=update.effective_message.message_thread_id,
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    upsert_user(user.id, user.username or "", user.first_name or "User")
    await update.message.reply_text("✅ تم تسجيلك.")


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return

    if not get_user_active(user.id):
        await update.message.reply_text("استخدم /register أولاً.")
        return

    msg = " ".join(context.args).strip()
    if not msg:
        await update.message.reply_text("اكتب إنجازك بعد الأمر.")
        return

    today = str(date.today())
    now = datetime.now()
    time_str = now.strftime("%I:%M %p").lstrip("0")
    now_iso = now.isoformat(timespec="seconds")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO daily_done (user_id, done_date, message, done_time, done_time_iso)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, done_date) DO UPDATE SET
            message=excluded.message,
            done_time=excluded.done_time,
            done_time_iso=excluded.done_time_iso
        """,
        (user.id, today, msg, time_str, now_iso),
    )

    cur.execute(
        "UPDATE users SET points = points + 1 WHERE user_id = ?",
        (user.id,),
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"🔥 تم تسجيل إنجازك الساعة {time_str} (+1 نقطة)"
    )


async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    today = str(date.today())

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT user_id, name FROM users WHERE active = 1")
    users = cur.fetchall()

    cur.execute("SELECT user_id FROM daily_done WHERE done_date = ?", (today,))
    done_ids = {r[0] for r in cur.fetchall()}

    conn.close()

    missing = [(uid, name) for uid, name in users if uid not in done_ids]

    if not missing:
        await send_in_topic(update, context, "🎉 الكل سجل اليوم.")
        return

    tags = "\n".join([f"- {mention(uid, name)}" for uid, name in missing])
    await send_in_topic(update, context, f"⏰ وينكم؟\n{tags}")


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    today = str(date.today())

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT user_id, name FROM users WHERE active = 1")
    users = cur.fetchall()

    cur.execute(
        """
        SELECT u.user_id, u.name, d.message, d.done_time
        FROM daily_done d
        JOIN users u ON u.user_id = d.user_id
        WHERE d.done_date = ? AND u.active = 1
        ORDER BY d.done_time_iso ASC
        """,
        (today,),
    )
    done_rows = cur.fetchall()

    done_ids = {r[0] for r in done_rows}
    missing = [(uid, name) for uid, name in users if uid not in done_ids]

    done_text = "✅ إنجازات اليوم:\n"
    if done_rows:
        done_text += "\n".join(
            [f"- {mention(uid, name)} ({t}): {msg}" for uid, name, msg, t in done_rows]
        )
    else:
        done_text += "ما في إنجازات."

    missing_text = "\n\n❌ لم يسجلوا اليوم:\n"
    if missing:
        missing_text += "\n".join([f"- {mention(uid, name)}" for uid, name in missing])
    else:
        missing_text += "ولا أحد 🎉"

    await send_in_topic(update, context, done_text + missing_text)

    cur.execute("DELETE FROM daily_done WHERE done_date = ?", (today,))
    conn.commit()
    conn.close()


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT name, points FROM users WHERE active = 1 ORDER BY points DESC"
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await send_in_topic(update, context, "لا يوجد مستخدمين.")
        return

    text = "🏆 النقاط:\n"
    text += "\n".join([f"- {name}: {pts}" for name, pts in rows])

    await send_in_topic(update, context, text)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    if not context.args:
        await update.message.reply_text("اكتب /remove @username")
        return

    ok = remove_user_by_username(context.args[0])
    await update.message.reply_text("✅ تم." if ok else "المستخدم غير موجود.")

async def update_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("استخدم:\n/updatePoints @username 7")
        return

    username = context.args[0].lstrip("@")

    try:
        new_points = int(context.args[1])
    except ValueError:
        await update.message.reply_text("النقاط لازم تكون رقم.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE username = ? AND active = 1",
        (username,),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        await update.message.reply_text("المستخدم غير موجود.")
        return

    cur.execute(
        "UPDATE users SET points = ? WHERE user_id = ?",
        (new_points, row[0]),
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ تم تحديث نقاط @{username} إلى {new_points}"

    )


async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("استخدم:\n/addPoints @username 2")
        return

    username = context.args[0].lstrip("@")

    try:
        points_to_add = int(context.args[1])
    except ValueError:
        await update.message.reply_text("القيمة لازم تكون رقم.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id, points FROM users WHERE username = ? AND active = 1",
        (username,),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        await update.message.reply_text("المستخدم غير موجود.")
        return

    user_id, current_points = row
    new_total = current_points + points_to_add

    cur.execute(
        "UPDATE users SET points = ? WHERE user_id = ?",
        (new_total, user_id),
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"✅ تم إضافة {points_to_add} نقطة لـ @{username}\nالمجموع الجديد: {new_total}"
    )

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_admin(user.id):
        await update.message.reply_text("للأدمن فقط.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE active = 1 AND points = 0"
    )
    users = cur.fetchall()

    if not users:
        conn.close()
        await update.message.reply_text("لا يوجد مستخدمين بنقاط 0.")
        return

    cur.execute(
        "UPDATE users SET active = 0 WHERE points = 0 AND active = 1"
    )

    conn.commit()
    conn.close()

    message = """
⚠️ تنبيه مهم بخصوص المتابعة

تم إزالة بعض المستخدمين من نظام المتابعة بسبب عدم وجود أي نشاط أو نقاط منذ بداية التحدي.

فكرة هذا الإشتراك أساساً قائمة على الالتزام اليومي والمتابعة الحقيقية للإنجاز. وجود أشخاص مسجلين بدون أي مشاركة أو إنجاز يخلق شعور عام بالتقصير ويؤثر على جو الالتزام عند باقي المشاركين الذين يحاولون فعلاً الاستمرار.

نُقدر ظروف الجميع، لكن في نفس الوقت الهدف من الاشتراك في التحدي ليس فقط الوجود في المجموعة، بل المشاركة الفعلية والعمل اليومي حتى لو كان الإنجاز بسيط.

إذا كان لديك ظرف أو سبب معين منعك من المشاركة خلال الفترة الماضية، يمكنك إرسال تبرير أو توضيح على الخاص حتى نراجع الخطة للفترة القادمة، وبعدها يمكنك التسجيل مرة أخرى.

الهدف ليس الإقصاء، بل الحفاظ على جدية التحدي وعدم التأثير على الأشخاص الملتزمين فعلاً والذين يحاولون الاستمرار يومياً.

بالتوفيق للجميع
"""

    await update.message.reply_text(message)

def main():
    if not TOKEN:
        raise RuntimeError("Set TOKEN environment variable")

    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("checkout", checkout))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("updatePoints", update_points))
    app.add_handler(CommandHandler("addPoints", add_points))
    app.add_handler(CommandHandler("warn", warn))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()