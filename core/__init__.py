from __future__ import absolute_import
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
from .celery import app as celery_app
   

__all__ = ('celery_app',)
