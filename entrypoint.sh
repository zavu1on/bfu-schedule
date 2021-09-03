#!/usr/bin/env sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py createadmin --username admin --password 5qBW6vEdKG --noinput --email anon@mail.com

exec gunicorn Schedule.wsgi:application --workers=4 -b 0.0.0.0:8000