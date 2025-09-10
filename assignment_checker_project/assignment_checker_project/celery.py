import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment_checker_project.settings')

# Initialize Celery with the project name
app = Celery('assignment_checker_project')

# Load configuration from Django settings with CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicitly set broker connection retry on startup for Celery 6.0+
app.conf.broker_connection_retry_on_startup = True

# Optionally, configure the pool to use solo or threads to avoid PermissionError on Windows
# Uncomment one of the following lines based on your preference:
# app.conf.worker_pool = 'solo'  # Use solo pool to disable multiprocessing
# app.conf.worker_pool = 'threads'  # Use threads pool for better Windows compatibility

# Load task modules from all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')