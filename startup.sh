export LANG=C.UTF-8

gunicorn — bind=0.0.0.0 — timeout 600 telebot.wsgi — workers 3 & python3 manage.py telegrambot & python3 manage.py telegrambot1