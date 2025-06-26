release: python manage.py migrate
web: gunicorn store_front.wsgi
worker: celery -A store_front worker