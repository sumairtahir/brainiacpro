from celery import Celery
import os

# Create a Celery instance
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'declutter.settings')
app = Celery('declutter')

# Configure Celery using settings from Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed Django apps
app.autodiscover_tasks()
