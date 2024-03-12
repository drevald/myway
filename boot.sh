python main.py compilemessages
python main.py collectstatic --noinput
python main.py migrate
exec gunicorn myway.wsgi:application --bind 0.0.0.0:$PORT --log-file -