gunicorn --bind=0.0.0.0 --timeout 600 telebot.wsgi & python manage.py telegrambot & python manage.py telegrambot1