from django.core.management.base import BaseCommand
from bot.bot_service import main

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        main()