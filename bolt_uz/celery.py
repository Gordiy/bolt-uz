# celery.py
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolt_uz.settings')

# Create an instance of Celery
app = Celery('bolt_uz', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in the Django app
app.autodiscover_tasks(settings.INSTALLED_APPS)
