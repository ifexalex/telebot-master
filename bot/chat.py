from telegram import *
from telegram.ext import *

from account.models import TelegramUser

# NOTICE, LOOP = range(2)

# def start_chat(update, context):
#     text = update.message.text
#     context.bot.send_message(chat_id=698485392, text=f"Message alert: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n message: {text}")
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     return NOTICE
# def notice_alert(update, context):
#     text = update.message.text
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     update.message.reply_text(f"UPDATE SENDING: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n message: {text}")
#     return LOOP

# def loop_chat(update, context):
#     text = update.message.text
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     context.bot.send_message(chat_id=698485392, text=f"Message notification: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n message: {text}")
#     return LOOP

# def cancel_chat(update, context):
#     """End the conversation."""
#     data =update.message.reply_text("Bye!")
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     TelegramUser.append_message_id(update.message.chat_id, data.message_id)
#     return ConversationHandler.END
