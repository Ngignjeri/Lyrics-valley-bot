import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


BOT_TOKEN = os.getenv("BOT_TOKEN")


def start(update, context):
    update.message.reply_text(
        "🎵 Send artist and song name.\nExample: Adele Hello"
    )


def get_lyrics(query):
    try:
        parts = query.split(" ", 1)
        if len(parts) < 2:
            return "Format: Artist SongName"

        artist = parts[0]
        title = parts[1]

        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        response = requests.get(url).json()

        if "lyrics" in response:
            return response["lyrics"]
        else:
            return "❌ Lyrics not found."
    except:
        return "⚠️ Error searching lyrics."


def msg(update, context):
    text = update.message.text
    update.message.reply_text("🔍 Searching...")
    lyrics = get_lyrics(text)
    update.message.reply_text(lyrics)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, msg))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()