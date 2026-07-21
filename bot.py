from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from ai import ask_ai
from database import init_db, get_history, save_history


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ИИ-бот.\n"
        "Просто отправь мне сообщение, и я отвечу.\n\n"
        "Команды:\n"
        "/help - помощь\n"
        "/clear - очистить память"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start\n"
        "/help\n"
        "/clear"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_history(update.effective_user.id, "")
    await update.message.reply_text("✅ История очищена.")async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Показываем, что бот печатает
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    history = await get_history(user_id)

    answer = await ask_ai(history, text)

    new_history = history + f"\nПользователь: {text}\nБот: {answer}"

    # Ограничиваем размер памяти
    if len(new_history) > 12000:
        new_history = new_history[-12000:]

    await save_history(user_id, new_history)

    await update.message.reply_text(answer)async def on_startup(app: Application):
    await init_db()


app = Application.builder().token(BOT_TOKEN).post_init(on_startup).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("clear", clear))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Бот запущен...")

app.run_polling()
