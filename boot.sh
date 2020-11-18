#! /bin/sh
python main.py compilemessages
python main.py collectstatic --noinput
exec gunicorn myway.wsgi:application --bind 0.0.0.0:$PORT --log-file -