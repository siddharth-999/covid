from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid.settings')

app = Celery('covid')

CELERY_TIMEZONE = 'UTC'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.conf.broker_url = settings.BROKER_URL
app.conf.broker_transport_options = settings.BROKER_TRANSPORT_OPTIONS
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.conf.accept_content = settings.CELERY_ACCEPT_CONTENT
app.conf.task_serializer = settings.CELERY_TASK_SERIALIZER
app.conf.result_serializer = settings.CELERY_RESULT_SERIALIZER

app.autodiscover_tasks()
