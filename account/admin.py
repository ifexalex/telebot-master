from django.contrib import admin
from .models import TelegramUser,TelegramSettings

admin.site.register(TelegramUser)
admin.site.register(TelegramSettings)
