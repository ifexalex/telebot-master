from telegram import *
from telegram.ext import *
import logging
import re

from account.models import TelegramUser

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

SUCCESS, UPDATE_ADDRESS,  UPDATE_EMAIL,  UPDATE_PHONE,  UPDATE_COUNTRY, UPDATE = range(6)


# check if email is valid or not: returns true if valid, false if not
def is_valid_email(email):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"  # check if email is valid
    return bool((re.search(regex, email)))


def is_valid_phone_number(phone_number):
    regex = "(?:(?:(\s*\(?([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\)?\s*(?:[.-]\s*)?)([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})"
    return bool((re.search(regex, phone_number)))


def start_update(update, context):
    """
    Updates the user's information.
    """
    # A function that is used to store the message id of the user.
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    reply_keyboard = [["Address", "Email", "Phone", "Country"]]

    _message_id = update.message.reply_text(
        "Hey! Select the information you want to update:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select the information you want to update",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    return UPDATE


def select_update(update, context):
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    reply_keyboard = [["continue"]]

    _message_id =update.message.reply_text(
        f"You selected to update: {text}" + "\n" + "Do you want to continue?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            force_reply=True,
            input_field_placeholder="continue or cancel",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)

    if text == "Address":
        return UPDATE_ADDRESS
    elif text == "Country":
        return UPDATE_COUNTRY
    elif text == "Email":
        return UPDATE_EMAIL
    elif text == "Phone":
        return UPDATE_PHONE


def update_email(update, context):
    """Stores the email of the user."""
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if not is_valid_email(text):
        _message_id_1= update.message.reply_text(
            f"""
            *Email address is invalid: Please enter a valid email* \n
            """,
            parse_mode=ParseMode.MARKDOWN,
        )
        TelegramUser.append_message_id(update.message.chat_id, _message_id_1.message_id)

        return UPDATE_EMAIL
    else:
        _message_id = update.message.reply_text(
            "Enter your updated email address",
            reply_markup=ReplyKeyboardRemove(),
        )
        TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
        return SUCCESS


def update_phone(update, context):
    """Stores the phone number of the user."""
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if not is_valid_phone_number(text):
        _message_id_1 = update.message.reply_text(
            f"""
            *Phone number is invalid: Please enter a valid phone number* \n
            """,
            parse_mode=ParseMode.MARKDOWN,
        )
        TelegramUser.append_message_id(update.message.chat_id, _message_id_1.message_id)
        return UPDATE_PHONE
    else:
        _message_id=update.message.reply_text(
            "Enter your updated phone number",
            reply_markup=ReplyKeyboardRemove(),
        )
        TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
        return SUCCESS


def update_address(update, context):
    """Stores the selected address and asks for country."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    _message_id = update.message.reply_text(
        "Enter your updated address",
        reply_markup=ReplyKeyboardRemove(),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)

    return SUCCESS


def update_country(update, context):
    """Stores the country of the user."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    _message_id = update.message.reply_text(
        "Enter your updated country",
        reply_markup=ReplyKeyboardRemove(),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)

    return SUCCESS


def update_succesful(update, context):
    """Send a message when the command is called."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    _message_id = update.message.reply_text("Update successful!")
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)

    return ConversationHandler.END


def update_cancel(update, context):
    """End the conversation."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    _message_id = update.message.reply_text("Profile update process cancelled.")
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)

    return ConversationHandler.END
