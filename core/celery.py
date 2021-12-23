from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from api.tasks import scraping_periodic_task

app = Celery('core')
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    
    'setup_periodic_task': {
        'task': 'api.tasks.scraping_periodic_task',
        'schedule': 20.0,
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
