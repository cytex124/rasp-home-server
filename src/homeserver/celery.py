from __future__ import absolute_import
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserver.settings.local')

app = Celery('homeserver')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(packages=["addons.price_control", "addons.odoo_sales_check"])
