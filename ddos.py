import os
import json
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# আপনার টোকেন এবং চ্যাট আইডি
BOT_TOKEN = "8933321937:AAHYwCWFAkmi0Q8taHhYrWImaA75KsG6mC4"
CHAT_ID = -1003945796522  

DATA_FILE = "users.json"

# ডাটাবেজ লোড করার ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

# ডাটাবেজ সেভ করার ফাংশন
def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data: {e}")

# ১. /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "⚡ **Ultra Boost User Management Bot** ⚡\n\n"
        "🛠 **Available Commands:**\n"
        "• `/adduser username password days` - নতুন ইউজার ও মেয়াদের দিন সেট করুন\n"
        "• `/users` - মোট ইউজার তালিকা ও মেয়াদ দেখুন\n"
        "• `/block username` - ইউজার ব্লক এবং ডিলিট করুন\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ২. /adduser কমান্ড
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("❌ **সঠিক নিয়ম:** `/adduser username password days`", parse_mode="Markdown")
        return

    username = args[0].strip()
    password = args[1].strip()
    try:
        days = int(args[2])
    except ValueError:
        await update.message.reply_text("❌ **মেয়াদের দিন সংখ্যা অবশ্যই সংখ্যা (Number) হতে হবে!**", parse_mode="Markdown")
        return

    data = load_data()
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

    data[username] = {
        "password": password,
        "expiry": expiry_date,
        "status": "Active"
    }
    save_data(data)

    await update.message.reply_text(
        f"✅ **User Created Successfully!**\n\n"
        f"👤 **Username:** `{username}`\n"
        f"🔑 **Password:** `{password}`\n"
        f"⏳ **Validity:** {days} Days\n"
        f"📅 **Expiry Date:** `{expiry_date}`",
        parse_mode="Markdown"
    )

# ৩. /users কমান্ড
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data:
        await update.message.reply_text("📂 **কোনো ইউজার পাওয়া যায়নি!**", parse_mode="Markdown")
        return

    msg = f"📊 **Total Active Users: {len(data)}**\n\n"
    for user, info in data.items():
        msg += (
            f"👤 **User:** `{user}`\n"
            f"🔑 **Pass:** `{info['password']}`\n"
            f"📅 **Exp:** `{info['expiry']}`\n"
            f"⚡ **Status:** {info['status']}\n"
            f"-------------------------\n"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")

# ৪. /block কমান্ড
async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❌ **সঠিক নিয়ম:** `/block username`", parse_mode="Markdown")
        return

    username = args[0].strip()
    data = load_data()

    if username in data:
        del data[username]  
        save_data(data)
        await update.message.reply_text(f"🚫 **User `{username}` সফলভাবে ব্লক এবং রিমুভ করা হয়েছে!**", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ **`{username}` নামের কোনো ইউজার খুঁজে পাওয়া যায়নি!**", parse_mode="Markdown")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("block", block_user))

    print("🤖 Ultra Boost Admin Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
