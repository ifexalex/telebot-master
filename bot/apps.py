from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    # def ready(self):
    #     import bot.telethon_bot
        # import bot.bot_service
