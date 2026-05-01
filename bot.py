import base64
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BLOG_REDIRECT = "https://achiveanimeencodes.blogspot.com/p/redirect.html#"

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

def encode_url(url: str) -> str:
    first = base64.b64encode(url.encode()).decode()
    second = base64.b64encode(first.encode()).decode()
    return second

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    if update.message and update.message.text:
        url = update.message.text.strip()

        if url.startswith("http"):
            token = encode_url(url)
            final = BLOG_REDIRECT + token
            await application.bot.send_message(
                chat_id=update.message.chat.id,
                text=f"🔗 Your Redirect Link:\n{final}"
            )
        else:
            await application.bot.send_message(
                chat_id=update.message.chat.id,
                text="Send a valid URL starting with http/https"
            )

    return "ok"
