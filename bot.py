import os
import time
import requests
from collections import deque
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8772166036:AAHQFThKIvB5Oc7kpa3FOQO1IZEM46luRCw")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

TARGET_URL = os.getenv("TARGET_URL", "https://example.com")

WINDOW = 60
ALERT_THRESHOLD = 100

requests_log = deque()


def check_traffic():
    now = time.time()

    while requests_log and now - requests_log[0] > WINDOW:
        requests_log.popleft()

    try:
        r = requests.get(TARGET_URL, timeout=10)
        requests_log.append(now)

        return r.status_code, len(requests_log)

    except requests.RequestException:
        return 0, len(requests_log)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ DDoS Monitor Bot\n\n"
        "📊 /status - Server status\n"
        "🔎 /check - Traffic check\n"
        "ℹ️ /help - Commands"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code, traffic = check_traffic()

    if code == 0:
        msg = "🔴 Server unreachable!"
    else:
        msg = f"🟢 Server online\nHTTP: {code}"

    msg += f"\n📊 Checks in last {WINDOW}s: {traffic}"

    if traffic >= ALERT_THRESHOLD:
        msg += "\n\n🚨 HIGH TRAFFIC DETECTED!"

    await update.message.reply_text(msg)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code, traffic = check_traffic()

    if traffic >= ALERT_THRESHOLD:
        text = (
            "🚨 সম্ভাব্য অস্বাভাবিক ট্রাফিক!\n\n"
            f"📊 Requests/checks: {traffic}\n"
            f"🌐 HTTP: {code}\n"
            "🛡️ Server-side rate limiting চালু করুন।"
        )

        if ADMIN_ID:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=text
            )

    await update.message.reply_text(
        f"🔎 Check complete\nHTTP: {code}\n"
        f"📊 Activity: {traffic}"
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("check", check))

    print("🛡️ DDoS Monitor Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
