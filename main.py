import os
import random
import logging
from   uuid import uuid4
from   dotenv import load_dotenv

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    ContextTypes,
)

# Load environment variables (useful in local dev)
load_dotenv()

BOT_USERNAME = os.getenv("BOT_USERNAME", "lgbtmetro_bot")

# LGBT+ identities with emojis
orientations = {
    "gay":         "🏳️‍🌈",
    "lesbian":     "👭",
    "bisexual":    "💖💜💙",
    "transgender": "⚧️",
    "asexual":     "🖤🤍💜",
    "pansexual":   "💗💛💙",
    "non-binary":  "💛⚫💜",
    "queer":       "🏳️‍🌈✨",
    "intersex":    "💛⚪",
    "demisexual":  "⚪💜🖤",
}

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🌈 Welcome to the Inline LGBT+ Identity Calculator™️!\n\nType in any chat:\n"
        + "\n".join([f"@{BOT_USERNAME} {o}" for o in orientations])
        + "\n\n(Just for fun! Love and respect all identities ❤️)"
    )

# Inline query
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower().strip()
    logger.info(f"Received inline query: '{query}'")

    results = []

    # Match query to identities
    for orientation in orientations:
        if query in orientation:
            percentage = random.randint(0, 100)
            emoji = orientations[orientation]
            text = f"🌈 You're {percentage}% *{orientation.capitalize()}* {emoji}!"
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"{orientation.capitalize()} {emoji}",
                    input_message_content=InputTextMessageContent(text, parse_mode="Markdown"),
                    description=f"Test if I am {orientation}...",
                )
            )

    if not results:
        for orientation in orientations:
            percentage = random.randint(0, 100)
            emoji = orientations[orientation]
            text = f"🌈 You're {percentage}% *{orientation.capitalize()}* {emoji}!"
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"{orientation.capitalize()} {emoji}",
                    input_message_content=InputTextMessageContent(text, parse_mode="Markdown"),
                    description=f"{percentage}% {orientation}",
                )
            )

    await update.inline_query.answer(results, cache_time=1)

# Entry point
def main():
    token = os.getenv("TOKEN")
    if not token:
        logger.error("❌ TOKEN environment variable not set.")
        return

    try:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(InlineQueryHandler(inline_query))

        logger.info("✅ Bot is starting...")
        app.run_polling()
    except Exception as e:
        logger.exception(f"🚨 Bot failed to start: {e}")

if __name__ == "__main__":
    main()
