import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚖️ مرحبا في بوت UFC حقوق سنة أولى!\nابعثلي سؤالك و نجاوبك!")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    await update.message.reply_text(f"سؤالك: {q}\nجاري البحث في دروس السنة الأولى...")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
app.run_polling()
