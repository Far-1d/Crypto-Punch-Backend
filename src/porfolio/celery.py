import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'porfolio.settings')

app = Celery('porfolio')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['news', 'asset'])