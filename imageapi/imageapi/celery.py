
import os
from celery import Celery
from . import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageapi.settings')

app = Celery('imageapi')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)