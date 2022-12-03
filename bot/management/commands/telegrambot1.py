from django.core.management.base import BaseCommand
from bot.telethon_bot import client_1

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        client_1