#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from cgitb import text
from email import message
import logging
from multiprocessing import context
from decouple import config
from django.dispatch import receiver
from telegram import *
from telegram.ext import *
from account.models import TelegramUser
from crypto.models import CryptoCurrency, CryptoNetwork, Wallets
import coinaddrvalidator
import re


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    firstname = update.message.from_user.first_name


    # print(username, chat_id, fullname, message_id)
    _message_id_1 = update.message.reply_text(
        f"""Hello *{firstname}*! \n
Welcome to the Cornix Messager Bot! \n
        """,
        parse_mode=ParseMode.MARKDOWN,
    )

    reply_keyboard = [
        [
            "/send message",
            "/settings"
        ]
    ]

    _message_id_2 = update.effective_message.reply_text(
        f"""
         Select an action you want to perform \n
        """,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )

def send_message(update, context):
    text = update.message.text

    context.bot.send_message(
        
    )



def invalid(update, context):
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/send message"], ["/settings"]]
    
    message_ = update.message.reply_text(
            f"""
            🚫 *Invalid command* 🚫 \n
Please use one of the following commands: \n
/send message 
/settings .
    """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                resize_keyboard=True,
                input_field_placeholder="/start",
            ),
    )


def echo(update, context):
    """Echo the user message."""
    text = update.message.text

    if text in ["/start", "start"]:
        start(update, context) 
    elif text in ["/send message", "send message"]:
        send_message(update, context)
    elif text in ["/settings", "settings"]:
        settings(update, context)
        
    else:
        invalid(update, context)
        



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)




start_handler = CommandHandler("start", start)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config("TELEGRAM_BOT_TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # dp.add_handler(chat_handler)
    

    dp.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command | Filters.regex('^(Back 🔙|Change wallet 🔙)'),

            echo,
        )
    )

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
