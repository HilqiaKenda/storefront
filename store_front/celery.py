import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_front.settings.dev')

celery = Celery('store_front')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()