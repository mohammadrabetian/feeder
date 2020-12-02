#!/bin/bash
echo "<---Waiting for database creation--->"
sleep 10

echo "<---Apply database migrations--->"
python manage.py migrate

echo "<---Starting server--->"
echo "Starting $NAME as `whoami`"

echo "django settings: $DJANGO_SETTINGS_MODULE "
gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=0.0.0.0:8000 \
  --reload \
  --log-level=$LOG_LEVEL \
  --log-file=- || sleep 10000 
