#!/usr/bin/bash

python manage.py migrate --no-input
celery -A concertify worker --uid=nobody --gid=nogroup &
python manage.py runserver 0.0.0.0:8000
