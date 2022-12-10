
from telnetlib import ECHO
from telegram import *
from telegram.ext import *
import logging
import re
import coinaddrvalidator
from account.models import TelegramUser
from crypto.models import CryptoCurrency, CryptoNetwork, Wallets
from investment.models import InvestmentPlan
from helpers.SendEmail import send_mail

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


START, WITHDRAWAL_NETWORK, ECHO_UPLOAD, UPLOAD_QRCODE,CONFIRM_PLAN,SELECT_PAYOUT_WALLET,CONFIRM_PAYOUT_WALLET,TXN_HASH,FINISHED, ECHO, CHAT, MENU= range(12)

def subscribe(update, context):
    text = str(update.message.text)

    reply_keyboard = [["Yes 🔔", "No 🔕"]]
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    _message_id=update.message.reply_text(
        f"""
        *You are about to take a bold step to financial freedom 🤑* \n
Are you sure you want to subscribe to Cornix premium? \n
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Select Yes or No",
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    
    return START

def select_withdrawal_coin(update, context):
    text = update.message.text
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if text == "No 🔕":
        TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
        return cancel_subscription(update, context)
    coins = CryptoCurrency.objects.all()
    reply_keyboard = [[coin.symbol for coin in coins],["Back 🔙"]]
    bot_message =update.message.reply_text(
        f"""
        *Select your preferred withdrawal coin:* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Select Coin",
            force_reply=True,
        )
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return WITHDRAWAL_NETWORK


def select_withdrawal_network(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if text in {"BTC", "ETH", "LTC"}:
        return echo_upload(update, context)
    if text == "Back 🔙":
        TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
        return select_withdrawal_coin(update, context)
    # elif text in {"BNB", "BUSD"}:
    #     networks = CryptoNetwork.objects.filter(name__in=["Beacon Chain (BEP2)","BNB Chain (BEP20)","Ethereum (ERC20)"])
    #     reply_keyboard = [[network.name for network in networks], ["Back 🔙"]]

    #     bot_message = update.message.reply_text(
    #     f"""
    #     *Select your preferred network for withdrawal* \n
    #     """,
    #     parse_mode= ParseMode.MARKDOWN,
    #     reply_markup=ReplyKeyboardMarkup(
    #         reply_keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="Select Network",
    #         resize_keyboard=True,
    #     )
    #     )
    #     TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    #     return ECHO_UPLOAD


    elif text == "USDT":
        networks_1 = CryptoNetwork.objects.filter(name__in=["Beacon Chain (BEP2)", "Ethereum (ERC20)","BNB Chain (BEP20)","Tron (TRC20)"])[:2]
        networks_2 = CryptoNetwork.objects.filter(name__in=["Beacon Chain (BEP2)", "Ethereum (ERC20)","BNB Chain (BEP20)","Tron (TRC20)"])[2:]
        reply_keyboard = [[network.name for network in networks_1],[network.name for network in networks_2] ,["Back 🔙"]]
        bot_message = update.message.reply_text(
        f"""
        *Select your preferred network for withdrawal* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select Network",
            resize_keyboard=True,
        )
        )
        TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
        return ECHO_UPLOAD


def echo_upload(update, context):
    """Stores the selected gender and asks for a photo."""
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

    if text == "Back 🔙":
        TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
        return select_withdrawal_network(update, context)

    reply_keyboard = [["/skip"]]

    bot_message = update.message.reply_text(
        f"""
        *Upload an image of your wallet QRcode* \n
if you don't have the QRcode image, you can click /skip to skip this step
        
Note: *You can paste the address manually if you don't have the QRcode image in the next step.*\n
""",
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Click to skip to the next step",
        )
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return UPLOAD_QRCODE



def upload_qrcode(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("user_photo.jpg")
    bot_message = update.message.reply_text(
        f"""
        *Paste your wallet address here 👇🏻* \n
Note: *It is recommended to copy the address from your exchanger and paste it below*\n
""",
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return CONFIRM_PLAN


def skip_upload_qrcode(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    bot_message = update.message.reply_text(
        f"""
        *Paste your wallet address here 👇🏻* \n
Note: *It is recommended to copy the address from your exchanger and paste it below*\n
""",
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return CONFIRM_PLAN



# def select_subscription_plan(update, context):
#     text = update.message.text
#     TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)

#     if text == "Back 🔙":
#         TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
#         return select_withdrawal_coin(update, context)
#     plans = InvestmentPlan.objects.all()
#     reply_keyboard = [[plan.name for plan in plans], ["Back 🔙"]]
#     bot_message = update.message.reply_text(
#         f"""
#         *Select the plan you want to subscribe to* \n
#         """,
#         parse_mode= ParseMode.MARKDOWN,
#         reply_markup=ReplyKeyboardMarkup(
#             reply_keyboard,
#             one_time_keyboard=True,
#             resize_keyboard=True,
#             input_field_placeholder="Select Plan",
#         )
#     )
#     TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
#     return CONFIRM_PLAN


def confirm_selected_plan(update, context):
    """Echo the user message."""
    text = str(update.message.text)
    if text == "Back 🔙":
        return echo_upload(update, context)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    selected_plan = InvestmentPlan.objects.all().first()
    button = [
        [
            InlineKeyboardButton("Proceed ✅", callback_data="proceed")
        ],
        [
            InlineKeyboardButton("Cancel 🚫", callback_data="cancel")
        ],
    ]
    bot_message = context.bot.send_message(
        chat_id=update.message.chat_id,
        text= f"""{selected_plan.description}""",
        reply_markup=InlineKeyboardMarkup(button),
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)


def select_payout_wallet(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    if text == "Back 🔙":
        TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
        return echo_upload(update, context)

    wallets_1 = Wallets.objects.all()
    reply_keyboard = [[wallet.name for wallet in wallets_1],["Back 🔙"]]
    bot_message = update.message.reply_text(
        f"""
        *Select the wallet you want to pay with* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Select Wallet",
        )
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return CONFIRM_PAYOUT_WALLET

def confirm_paying_wallet(update, context):
    """Echo the user message."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    text = update.message.text
    selected_wallet = Wallets.objects.get(name=str(text))
    button = [
        [
            InlineKeyboardButton("Paid 💰", callback_data="paid")
        ],
        [
            InlineKeyboardButton("Change wallet 🔙", callback_data="cancel")
        ],

    ]
    bot_message = update.message.reply_text(
        f"""\n
        `{selected_wallet.address}`
        """,
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)

    # context.bot.send_message(
    #     chat_id=update.message.chat_id,
    #     text= f"""\n
    #     `{selected_wallet.address}`
    #     """,
    #     parse_mode= ParseMode.MARKDOWN,
    # )
    img_url = "path"

    if 'ETH' in text:
        img_url = "static/images/eth_qrcode.jpg"
    elif "Bitcoin" in text:
        img_url = "static/images/btc_qrcode.jpg"
    elif "USDT" in text:
        img_url = "static/images/usdt_qrcode.jpg"



    bot_message_1 = context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo= open(img_url, "rb"),
        caption= f"""\n
*Please send the amount you want to pay to the above address* \n
*Below is the wallet full details: * \n
*Coin:* _{selected_wallet.cryptocurrency.symbol}_
*address:* _{selected_wallet.address}_
*Network:* _{selected_wallet.network}_\n
_Note: Payment is expected to be received within 12hours_\n
_After payment, you are required to copy the transaction hash as you
will be submitting it for confirmation in the next step._\n
""",
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(button),
    )

#     bot_message_1 = context.bot.send_message(
#         chat_id=update.message.chat_id,
#         text= f"""\n
# *Please send the amount you want to pay to the above address* \n
# *Below is the wallet full details: * \n
# *Coin:* _{selected_wallet.cryptocurrency.symbol}_
# *address:* _{selected_wallet.address}_
# *Network:* _{selected_wallet.network}_\n
# _Note: Payment is expected to be received within 12hours_\n
# _After payment, you are required to copy the transaction hash as you
# will be submitting it for confirmation in the next step._\n
# """,
#         reply_markup=InlineKeyboardMarkup(button),
#         parse_mode= ParseMode.MARKDOWN,   
#     )
    TelegramUser.append_message_id(update.message.chat_id, bot_message_1.message_id)
    user = TelegramUser.objects.get(chat_id=update.message.chat_id)
    send_mail(
                "Payment Request",
                "index.html",
                "Cornix Premium <noreply@gmail.com>",
                [user.email],
                context_dict={
                    "full_name": update.message.from_user.full_name,

                }
            )
    return TXN_HASH

def submit_transaction_hash(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    bot_message = update.message.reply_text(
        f"""
        *Enter the Txid/transaction Hash:* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return FINISHED


def complete_subscription(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["speak with an admin 📞"], ["Menu"]]
    bot_message = update.message.reply_text(
        """
        *Great! You are done with the subscription process.* \n
*Wait for confirmation and Admin approval of subscription* \n

*Note:* _We just sent you an email._
_Can't find the email? kindly check your spam or junk folder._
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup= ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Select an option",
        )
    )
    notice = context.bot.send_message(chat_id=5337326469, text=f"user detail below has marked as paid: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n txn_hash: {text}")
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    TelegramUser.append_message_id(update.message.chat_id, notice.message_id)
    return CHAT

def echo_transfer(update, context):
    text = str(update.message.text)
    if text == "Menu":
        return menu(update, context)
    elif text == "speak with an admin 📞":
        bot_message = update.message.reply_text("""
        *You are now being transferred to an admin support representative* \n
        """, parse_mode=ParseMode.MARKDOWN)

        notice_admin_1= context.bot.send_message(chat_id=5586325071, text=f"user have requested for a chat: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n txn_hash: {text}")
        notice_admin_2 = context.bot.send_message(chat_id=5337326469, text=f"user have requested for a chat: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n txn_hash: {text}")

        TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
        TelegramUser.append_message_id(update.message.chat_id, notice_admin_1.message_id)
        TelegramUser.append_message_id(update.message.chat_id, notice_admin_2.message_id)
        return CHAT

def start_chat(update, context):
    text = update.message.text
    if text == "Menu":
        return menu(update, context)
    context.bot.send_message(chat_id=5586325071, text=f"Message alert: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n message: {text}")
    context.bot.send_message(chat_id=5337326469, text=f"Message alert: \n username: {update.message.from_user.username}\nuser_id: {update.message.chat_id} \n message: {text}")
    txt =update.message.reply_text(
        """Hold on while we respond to your message. You can click /subscribe to return to subscription. \n Note: please ensure admin confirms your subscription before clicking /subscribe""",
    )
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    TelegramUser.append_message_id(update.message.chat_id, txt.message_id)
    return CHAT    


def cancel_subscription(update, context):
    text = str(update.message.text)
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    bot_message = update.message.reply_text(
        f"""
        *You have cancelled the subscription process.* \n
*Please try again later.* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
    )
    TelegramUser.append_message_id(update.message.chat_id, bot_message.message_id)
    return ConversationHandler.END


def menu(update, context):
    """Stores the country of the user."""
    TelegramUser.append_message_id(update.message.chat_id, update.message.message_id)
    reply_keyboard = [["/subscribe"],["/updateInformation"],["Signal Report 📈", "/help"]]

    _message_id = update.message.reply_text(
        """
        *Thank you for choosing Cornix* \n
        """,
        parse_mode= ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Select an option",
            resize_keyboard=True,
        ),
    )
    TelegramUser.append_message_id(update.message.chat_id, _message_id.message_id)
    return ConversationHandler.END


def confirm_plan_callback(update, context):
    query = update.callback_query
    if query.data == "proceed":
        return select_payout_wallet(update.callback_query, context)
    else:
        return echo_upload(update.callback_query, context)

def confirm_wallet_callback(update, context):
    query = update.callback_query
    if query.data == "paid":
        return submit_transaction_hash(update.callback_query, context)
    elif query.data == "cancel":
        return select_payout_wallet(update.callback_query, context)
    
