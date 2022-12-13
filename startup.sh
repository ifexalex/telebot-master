export LANG=C.UTF-8

gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 --chdir telebot telebot.wsgi & python manage.py telegrambot