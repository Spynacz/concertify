#!/usr/bin/bash

python manage.py migrate --no-input
redis-server &
celery -A concertify worker &
python manage.py runserver 0.0.0.0:8000 