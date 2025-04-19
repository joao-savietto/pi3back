import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi3back.settings")

app = Celery("pi3back")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
