gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 telebot.wsgi --access-logfile '-' --error-logfile '-' & python manage.py telegrambot & python manage.py telegrambot1