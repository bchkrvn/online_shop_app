import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
os.environ.setdefault('RABBITMQ_DEFAULT_USER', 'shop')
os.environ.setdefault('RABBITMQ_DEFAULT_PASS', 'shop')

app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
