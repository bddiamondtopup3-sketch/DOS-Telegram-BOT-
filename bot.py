import os
import json
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# আপনার দেওয়া ইনফো
BOT_TOKEN = "8933321937:AAHYwCWFAkmi0Q8taHhYrWImaA75KsG6mC4"
CHAT_ID = -1003945796522  # চ্যাট আইডি (প্রয়োজনে অ্যাডমিন চেক করতে পারেন)

DATA_FILE = "users.json"

# ইউজার ডেটা লোড বা সেভ করার ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "⚡ **Ultra Boost User Management Bot** ⚡\n\n"
        "🛠 **Commands:**\n"
        "• /adduser `username` `password` `days` - নতুন ইউজার ও মেয়াদ তৈরি করুন\n"
        "• /users - মোট ইউজারের তালিকা ও মেয়াদ দেখুন\n"
        "• /block `username` - ইউজার ব্লক/রিমুভ করুন\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# নতুন ইউজার ও পাসওয়ার্ড তৈরি: /adduser user pass days
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("❌ সঠিক নিয়ম: `/adduser username password days`", parse_mode="Markdown")
        return

    username = args[0]
    password = args[1]
    try:
        days = int(args[2])
    except ValueError:
        await update.message.reply_text("❌ দিন সংখ্যা (days) অবশ্যই সংখ্যা হতে হবে!")
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
        f"👤 Username: `{username}`\n"
        f"🔑 Password: `{password}`\n"
        f"⏳ Validity: {days} Days (Exp: {expiry_date})",
        parse_mode="Markdown"
    )

# মোট ইউজার দেখার তালিকা: /users
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data:
        await update.message.reply_text("📂 কোনো ইউজার নেই!")
        return

    msg = f"📊 **Total Users: {len(data)}**\n\n"
    for user, info in data.items():
        msg += f"• **User:** `{user}`\n  **Pass:** `{info['password']}`\n  **Exp:** {info['expiry']}\n  **Status:** {info['status']}\n\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

# ইউজার ব্লক বা রিমুভ করা: /block username
async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❌ সঠিক নিয়ম: `/block username`", parse_mode="Markdown")
        return

    username = args[0]
    data = load_data()

    if username in data:
        del data[username] # ডাটাবেজ থেকে রিমুভ করে দেওয়া
        save_data(data)
        await update.message.reply_text(f"🗑️ User `{username}` সফলভাবে রিমুভ ও ব্লক করা হয়েছে!", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ `{username}` নামের কোনো ইউজার পাওয়া যায়নি!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("block", block_user))

    print("🤖 Admin Control Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
