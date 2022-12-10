from telegram import *
from telegram.ext import *
import logging
import re

from account.models import TelegramUser

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

EMAIL = range(1)


# check if email is valid or not: returns true if valid, false if not
def is_valid_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') # check if email is valid
    return bool((re.fullmatch(regex, email)))


def is_valid_phone_number(phone_number):
    regex = '(\+|00)(297|93|244|1264|358|355|376|971|54|374|1684|1268|61|43|994|257|32|229|226|880|359|973|1242|387|590|375|501|1441|591|55|1246|673|975|267|236|1|61|41|56|86|225|237|243|242|682|57|269|238|506|53|5999|61|1345|357|420|49|253|1767|45|1809|1829|1849|213|593|20|291|212|34|372|251|358|679|500|33|298|691|241|44|995|44|233|350|224|590|220|245|240|30|1473|299|502|594|1671|592|852|504|385|509|36|62|44|91|246|353|98|964|354|972|39|1876|44|962|81|76|77|254|996|855|686|1869|82|383|965|856|961|231|218|1758|423|94|266|370|352|371|853|590|212|377|373|261|960|52|692|389|223|356|95|382|976|1670|258|222|1664|596|230|265|60|262|264|687|227|672|234|505|683|31|47|977|674|64|968|92|507|64|51|63|680|675|48|1787|1939|850|351|595|970|689|974|262|40|7|250|966|249|221|65|500|4779|677|232|503|378|252|508|381|211|239|597|421|386|46|268|1721|248|963|1649|235|228|66|992|690|993|670|676|1868|216|90|688|886|255|256|380|598|1|998|3906698|379|1784|58|1284|1340|84|678|681|685|967|27|260|263)(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{4,20}$'
    return bool((re.search(regex, phone_number)))



def register(update, context):
    reply_keyboard = [["continue", "/cancel"]]
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    _message_id = update.message.reply_text(
        f"Hi! {update.message.from_user.first_name} . You will be required to provide some required information. \n"
        "Send /cancel to stop terminate the registration process.\n\n"
        "Please provide your email address?",
        reply_markup=ReplyKeyboardRemove(),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    return EMAIL


def email(update, context):
    """Stores the email of the user."""
    
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if not is_valid_email(text):
        _message_id_1=update.message.reply_text(
            f"""
            *Email address is invalid: Please enter a valid email* \n
            """,
            parse_mode= ParseMode.MARKDOWN,
        )
        TelegramUser.append_message_id(update.message.chat_id, _message_id_1.message_id)
        return EMAIL
    else:
        # TelegramUser.objects.filter(chat_id=update.message.chat_id).update(email=text)
        # _message_id = update.message.reply_text(
        #     "You are almost there! Enter your residence Address, "
        #     "or send /skip to skip this step.",
        #     reply_markup=ReplyKeyboardRemove(),
        # )
        # TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
        return skip_address(update,context)


# def phone(update, context):
#     """Stores the phone number of the user."""
#     text = update.message.text
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

#     if not is_valid_phone_number(text):
#         TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#         _message_id_1 = update.message.reply_text(
#             f"""
#             *Phone number is invalid: Please enter a valid phone number* \n
#             """,
#             parse_mode= ParseMode.MARKDOWN,
#         )
#         TelegramUser.append_message_id(update.message.chat_id, _message_id_1.message_id)
#         return PHONE
#     else:
#         _message_id = update.message.reply_text(
#             "You are almost there! Enter your residence Address, "
#             "or send /skip to skip this step.",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#         TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
#         return ADDRESS



def address(update, context):
    """Stores the selected address and asks for country."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈", "/help"]]

    _message_id = update.message.reply_text(
        f"Thank you {update.message.from_user.first_name}! Your details has been saved.\n"
        "You can now proceed with subscription.",
        
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select an option",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    return ConversationHandler.END

def skip_address(update, context):
    """
    Skips the address step.
    If the user skips the address step,
    then the user is asked to send the country.
    """
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈", "/help"]]
    _message_id = update.message.reply_text(
        f"Thank you {update.message.from_user.first_name}! Your details has been saved.\n"
        "You can now proceed with subscription.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select an option",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    return ConversationHandler.END

# def country(update, context):
#     """Stores the country of the user."""
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#     reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈", "/help"]]

#     _message_id = update.message.reply_text(
#         f"Thank you {update.message.from_user.first_name}! Your details has been saved.\n"
#         "You can now proceed with subscription.",

#         reply_markup= reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈", "/help"]]
#     )
#     TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
#     return ConversationHandler.END
    

def cancel_reg(update, context):
    """Ends the conversation."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈"]]

    _message_id = update.message.reply_text(
        "Bye! Hope we can talk again some day.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select an option",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    
    return ConversationHandler.END

    
