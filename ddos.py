import os
import random
from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# আপনার টেলিগ্রাম বট টোকেন
BOT_TOKEN = "9052736500:AAG4GcgVy7T6RNjzpj5lA95MP7RDabvQ0Uc"  

# আপনার পছন্দের ইমোজি লিস্ট (এখান থেকে যেকোনো একটি রেন্ডমলি সিলেক্ট হবে)
MY_EMOJIS = ["👍", "❤️", "🔥", "🥰", "⚡", "🏆", "💔", "😍"]

# অটো রিঅ্যাকশন হ্যান্ডলার
async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # যদি মেসেজ বা চ্যাট না থাকে, তবে স্কিপ করবে
    if not update.message or not update.message.chat:
        return

    # লিস্ট থেকে র‍্যান্ডম ইমোজি সিলেক্ট করা (আপনার জাভাস্ক্রিপ্ট কোডের মতো)
    do_emoji = random.choice(MY_EMOJIS)

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    try:
        # টেলিগ্রাম এপিআই ব্যবহার করে মেসেজে রিঅ্যাকশন পাঠানো
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=do_emoji, is_big=True)]
        )
    except Exception as e:
        print(f"Failed to send reaction: {e}")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing!")

    app = Application.builder().token(BOT_TOKEN).build()

    # কোনো কমান্ড নেই, গ্রুপ বা চ্যাটে যেকোনো মেসেজ আসলেই অটো রিঅ্যাকশন দেবে
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_react))

    print("🤖 Auto Reaction Bot is running successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
