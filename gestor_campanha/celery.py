# projeto/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_campanha.settings')

app = Celery('gestor_campanha')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
