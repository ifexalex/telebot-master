from email import message
from multiprocessing.dummy import Array
from django.db import models
import telegram
from django.db.models import F
from django.db.models.expressions import CombinedExpression, Value
from decouple import config
from django.contrib.postgres.fields import ArrayField
from django.db.transaction import atomic


class TelegramUser(models.Model):
    username = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)
    fullname = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message_id = ArrayField(
        models.CharField(max_length=255, 
        blank=True,
        null=True),
        default=list,
    )
    bot_message_id = ArrayField(
        models.CharField(max_length=255, 
        blank=True,
        null=True),
        default=list,
    )
    crypto_address = models.CharField(max_length=255, blank=True, null=True)    # E.g Bitcoin address
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @classmethod
    def subscribe(cls, username, chat_id, fullname, message_to_append,):
        obj, created = cls.objects.get_or_create(

            chat_id=chat_id,
        )
        obj.chat_id = str(chat_id)
        obj.username = str(username)
        obj.fullname = str(fullname)
        obj.message_id = CombinedExpression(F('message_id'), "||", Value([str(message_to_append)]))
        obj.save()
        return


    @classmethod
    def append_message_id(cls, chat_id, message_to_append):
        obj, created = cls.objects.update_or_create(
            chat_id=chat_id,
            defaults= {
                'message_id': CombinedExpression(F('message_id'), "||", Value([str(message_to_append)])),
                'bot_message_id': CombinedExpression(F('bot_message_id'), "||", Value([str(message_to_append)])),
            }
        )
        return obj

    def send_message(self, msg):
        telegram_bot = telegram.Bot(token=config("TELEGRAM_BOT_TOKEN"))
        max_text_size = 4000
        try:
            if len(msg) <= max_text_size:
                return telegram_bot.send_message(chat_id=self.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
            for i in range(0, len(msg), max_text_size):
                #    self.append_message_id(self.chat_id, msg[i:i+max_text_size])
               return telegram_bot.send_message(chat_id=self.chat_id, text=msg[i:i+max_text_size], parse_mode = telegram.ParseMode.MARKDOWN)


        except telegram.error.Unauthorized:
            self.is_active = False
            self.save()

    def clear_chat(self):
        telegram_bot = telegram.Bot(token=config("TELEGRAM_BOT_TOKEN"))
        try:
            message_id_list = list(dict.fromkeys(self.message_id))
            message_id_list.reverse()
            
            for message_id in message_id_list:
                telegram_bot.delete_message(chat_id=self.chat_id, message_id=message_id)

        except telegram.error.Unauthorized:
            self.is_active = False

        except telegram.error.BadRequest:
            pass

    def __str__(self):
        return f"{self.username} : {self.chat_id}"



class TelegramUserMessage(models.Model):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    message = models.TextField( max_length=4000, blank=True, null=True)

    def __str__(self):
        return f"{self.telegram_user.username} : {self.message}"
    

class TelegramSettings(models.Model):
    auto_send = models.BooleanField(default=False)
    auto_send_text = models.TextField(blank=True, null=True)
    bot_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Auto Send: {self.auto_send}: bot_status: {self.bot_status}"