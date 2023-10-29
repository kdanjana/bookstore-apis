#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn bookstore.wsgi:application -c gunicorn_config.py --log-level=debug --access-logfile=- --error-logfile=-