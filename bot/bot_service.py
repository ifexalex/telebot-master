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
from account.models import TelegramUser,TelegramSettings
from crypto.models import CryptoCurrency, CryptoNetwork, Wallets
import coinaddrvalidator
import re
from .conversation import (
    GENDER,
    PHOTO,
    LOCATION,
    BIO,
    gender,
    photo,
    location,
    skip_location,
    bio,
    cancel,
)
from .subscription import *
from .register import *
from .update_info import *
from investment.models import InvestmentPlan
from .chat import *

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

    TelegramUser.subscribe(
        update.message.from_user.username,
        update.message.chat_id,
        update.message.from_user.full_name,
        update.message.message_id,
    )

    if not TelegramSettings.objects.get(id=1).bot_status:
        # print(username, chat_id, fullname, message_id)
        _message_id_1 = update.message.reply_text(
        """Hello Premium Payment confirmation desk! 

Welcome to the Cornix Premium Bullish Bot! 

Using our premium system, we'll automate your crypto trading with advanced trading features, designed to minimize/terminate risks and maximize profits. 


Whether you're trading with a signal provider, on your own, or using TradingView alerts, our bot will do the heavy lifting for you.""",
        parse_mode=ParseMode.MARKDOWN,
    )

        reply_keyboard = [
        [
            "/register",
        ]
    ]
        TelegramUser.append_message_id(update.message.chat_id, _message_id_1.message_id)

        _message_id_2 = update.effective_message.reply_text(
        f"""
        *Are you ready to connect with Cornix Premium? 😎* \n
        """,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
        TelegramUser.append_message_id(update.message.chat_id, _message_id_2.message_id)
    else:
        off_notice(update, context)
    


def trade_signal(update, context):
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    firstname = update.message.from_user.first_name
    reply_keyboard = [["cancel 🚫"]]
    
    button = [
        [InlineKeyboardButton("proceed ✅", url="https://t.me/premiumsignals_report")]
    ]
    _message_id = context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Hi *{firstname}!*, you are about to proceed to Cornix Premium Signal Report. \n\n Do you want to proceed?",
        reply_markup=InlineKeyboardMarkup(button),
        parse_mode=ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)


def invalid(update, context):
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/start"], ["Signal Report 📈"], ["/updateInfo","/Subscribe"]]
    
    message_ = update.message.reply_text(
            f"""
            🚫 *Invalid command* 🚫 \n
Please use one of the following commands: \n
/start 
/help 

__Our customers are at the heart of what we do. Without you, 
__we would cease to exist. It will always be a pleasure to serve you.__ 

*Thank you for choosing Cornix Premium!😊*.
    """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                resize_keyboard=True,
                input_field_placeholder="/start",
            ),
    )
    TelegramUser.append_message_id(update.message.chat_id, message_.message_id)

def off_notice(update, context):
    message_ = update.message.reply_text(
            f"""
            🚫 *Subscription  Paused* 🚫 \n
subscription has been paused for now due to the number of required users has been reached \n
/start 
/help 

__Stay tuned for next week as another subscription window will be opened, 
__It will always be a pleasure to serve you.__ 

*Thank you for choosing Cornix Premium!😊*.
    """,
            parse_mode=ParseMode.MARKDOWN,
    )


def echo(update, context):
    """Echo the user message."""
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if text in ["/start", "start"]:
        start(update, context) 
    elif text in ["/register", "register"]:
        register(update, context)
    elif text in ["/updateInfo", "update details"]:
        start_update(update, context)
    elif text in ["Subscribe 🔓", "/subscribe", "subscribe"]:
        subscribe(update, context)
    elif text == "Signal Report 📈":
        trade_signal(update, context)
    elif not TelegramSettings.objects.get(id=1).bot_status and text not in ["Back 🔙","Change wallet 🔙"]:
        off_notice(update, context)
    elif text not in ["Back 🔙","Change wallet 🔙"]:
        invalid(update, context)
        

# def trade_signal_callback(update, context):
#     query = update.callback_query
#     if query.data == "proceed ✅":
#         query.edit_message_text(text="🔥 *Trade signal sent!* 🔥")
#         TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     elif query.data == "terminate 🚫":
#         query.edit_message_text(
#             text="You have terminated the subscription process. \n Try choosing another plan to subscribe again.",
#             parse_mode=ParseMode.MARKDOWN,
#         )
#         TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

#     else:
#         TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#         context.bot.send_message(chat_id=query.message.chat_id, text="invalid command")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO


# chat_handler = ConversationHandler(
#     entry_points=[CommandHandler('open_chat', start_chat)],
#     states={
#         NOTICE: [MessageHandler(Filters.text, notice_alert)],
#         LOOP: [MessageHandler(Filters.text & ~Filters.command, loop_chat)],
#     },
#     fallbacks=[CommandHandler("cancel", cancel_chat)],
#     allow_reentry=True,
# )

reg_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        # ADDRESS: [
        #     MessageHandler(Filters.text, address),
        #     CommandHandler("skip", skip_address),
        # ],
    },
    fallbacks=[CommandHandler("cancel", cancel_reg)],
    allow_reentry=True,
)

update_succesful_handler = ConversationHandler(
    entry_points=[CommandHandler("updateInfo", start_update)],
    states={
        UPDATE: [
            MessageHandler(
                Filters.regex("^(Address|Email|Phone|Country)$"), select_update
            )
        ],
        UPDATE_EMAIL: [MessageHandler(Filters.text & ~Filters.command, update_email)],
        UPDATE_PHONE: [MessageHandler(Filters.text & ~Filters.command, update_phone)],
        UPDATE_ADDRESS: [
            MessageHandler(Filters.text & ~Filters.command, update_address)
        ],
        UPDATE_COUNTRY: [
            MessageHandler(Filters.text & ~Filters.command, update_country)
        ],
        SUCCESS: [MessageHandler(Filters.text & ~Filters.command, update_succesful)],
    },
    fallbacks=[CommandHandler("cancel", update_cancel)],
    allow_reentry=True,
)

coin_list = [coin.symbol for coin in CryptoCurrency.objects.all()] + ["Back 🔙"]
network_list = [chain.name for chain in CryptoNetwork.objects.all()] + ["Back 🔙"]
plan_list = [plan.name for plan in InvestmentPlan.objects.all()] + [" Back🔙"]
wallet_list = [wallet.name for wallet in Wallets.objects.all()] + [" Back🔙"]

subscribe_handler = ConversationHandler(
    entry_points=[CommandHandler("subscribe", subscribe)],
    states={
        START: [
            MessageHandler(Filters.regex("^(Yes 🔔|No 🔕|)$"), select_withdrawal_coin)
        ],
        WITHDRAWAL_NETWORK: [
            MessageHandler(
                Filters.regex("(?=(" + "|".join(map(re.escape, coin_list)) + "))"),
                select_withdrawal_network,
            )
        ],
        ECHO_UPLOAD: [MessageHandler(Filters.text, echo_upload)],
        UPLOAD_QRCODE: [
            MessageHandler(Filters.photo | Filters.regex(r'Back'), upload_qrcode),
            CommandHandler("skip", skip_upload_qrcode),
        ],
        CONFIRM_PLAN: [
            MessageHandler(Filters.text, confirm_selected_plan),
            CallbackQueryHandler(confirm_plan_callback),
        ],
        SELECT_PAYOUT_WALLET: [
            MessageHandler(
                Filters.regex("(?=(" + "|".join(map(re.escape, wallet_list)) + "))"),
                select_payout_wallet,
            )
        ],
        CONFIRM_PAYOUT_WALLET: [
            MessageHandler(Filters.text, confirm_paying_wallet),
            CallbackQueryHandler(confirm_wallet_callback),
        ],
        TXN_HASH: [MessageHandler(Filters.text, submit_transaction_hash)],
        FINISHED: [MessageHandler(Filters.text, complete_subscription)],
        ECHO: [MessageHandler(Filters.text, echo_transfer)],
        CHAT: [MessageHandler(Filters.text & ~Filters.command, start_chat)],
        MENU: [MessageHandler(Filters.text & ~Filters.command, menu)],
    },
    fallbacks=[CommandHandler("cancel", update_cancel)],
    allow_reentry=True,
)


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
    if TelegramSettings.objects.get(id=1).bot_status:
        print("Bot status is off")
        dp.add_handler(
            MessageHandler(
                Filters.text | ~Filters.command | Filters.regex('^(Back 🔙|Change wallet 🔙)'),

                off_notice,

            )
        )
    else:
        print("Bot status is on")
        dp.add_handler(reg_handler)
        dp.add_handler(update_succesful_handler)
        dp.add_handler(subscribe_handler)

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(
            MessageHandler(
                Filters.text & Filters.command | Filters.regex('^(Back 🔙|Change wallet 🔙)'),

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
