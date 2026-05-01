import os
from urllib.parse import quote_plus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

REDIRECT_BASE = "https://achiveanimeencodes.blogspot.com/p/redirect.html?url="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me your download link.\nI will generate quality buttons for you."
    )

def build_buttons(user_url: str):
    encoded = quote_plus(user_url)

    buttons = [
        [
            InlineKeyboardButton(
                "📥 480p Download",
                url=f"{REDIRECT_BASE}{encoded}&q=480p"
            )
        ],
        [
            InlineKeyboardButton(
                "📥 720p Download",
                url=f"{REDIRECT_BASE}{encoded}&q=720p"
            )
        ],
        [
            InlineKeyboardButton(
                "📥 1080p Download",
                url=f"{REDIRECT_BASE}{encoded}&q=1080p"
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_url = update.message.text.strip()

    if not user_url.startswith("http"):
        await update.message.reply_text("Please send a valid URL.")
        return

    keyboard = build_buttons(user_url)

    await update.message.reply_text(
        "Choose quality to download:",
        reply_markup=keyboard
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("Bot is running...")
    app.run_polling()
