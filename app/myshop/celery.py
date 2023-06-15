import os

from celery import Celery

app = Celery('myshop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
