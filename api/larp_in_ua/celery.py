import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "larp_in_ua.settings")

celery_app = Celery("larp_in_ua")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
