from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from datetime import datetime
import threading

BOT_TOKEN = "8390719066:AAFLtGfqaHBlZWHYr4WA9Hff_p-q6nMgb1Q"

app = Flask(__name__)
last_seen = None

@app.route("/ping", methods=["POST"])
def ping():
    global last_seen
    last_seen = datetime.utcnow()
    return "ok"

async def lastseen_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if last_seen is None:
        await update.message.reply_text("No activity recorded yet.")
    else:
        await update.message.reply_text(
            f"Laptop last active at (UTC): {last_seen.strftime('%Y-%m-%d %H:%M:%S')}"
        )

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("lastseen", lastseen_cmd))
    application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

app.run(host="0.0.0.0", port=10000)
