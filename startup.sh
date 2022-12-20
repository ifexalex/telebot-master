gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 --chdir telebot.wsgi & python3 manage.py telegrambot & python3 manage.py telegrambot1
