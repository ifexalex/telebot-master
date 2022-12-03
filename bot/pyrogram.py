import contextlib
import time, asyncio
from decouple import config
from pyrogram import *
from pyrogram.types import *

from account.models import TelegramUser

app = Client(
    "filename", # Will create a file named filename.session which will contain userbot "cache"
    # You could also change "filename" to ":memory:" for better performance as it will write userbot session in ram
    api_id="14323467", # You can get api_hash and api_id by creating an app on
    api_hash = "aa4063e9e0329f7de5fc240f099e6fc4", # my.telegram.org/apps (needed if you use MTProto instead of BotAPI)
    bot_token = config('TELEGRAM_BOT_TOKEN'), # Your bot token from @BotFather
)


@app.on_message(filters.command("start"))
async def start(app, message):
    await app.send_message(
        message.chat.id,
        """🚫 **Invalid command** 🚫 \n
Please use one of the following commands: \n
/start
/help

__Our customers are at the heart of what we do. Without you,
__we would cease to exist. It will always be a pleasure to serve you.__

    **Thank you for choosing Cornix Premium!😊**.""",
        
    )

@app.on_message(filters.command("help"))
async def help(app, message):
    await TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    await app.send_message(
    message.chat_id, "Look at that button!",
    reply_markup=ReplyKeyboardMarkup([["Nice!"]]))


@app.on_message(filters.me & filters.command("clearchat") & ~filters.private)
async def clearchat(client, message):
    chats = TelegramUser.objects.get(chat_id="698485392")

    for chat in chats:
        await client.delete_messages(chat.chat_id, chat.message_id)
        print(f"Deleted {chat.chat_id}")
        time.sleep(1)



app.run()
