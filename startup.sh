gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 telegrambot.wsgi & python manage.py telegrambot & python manage.py telegrambot1 --access-logfile '-' --error-logfile '-'