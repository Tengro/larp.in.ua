from ..django import TIME_ZONE as DJANGO_TIME_ZONE
from ..environment import env
from celery.schedules import crontab


CELERY_TASK_ALWAYS_EAGER = env.bool("LARP_IN_UA_CELERY_TASK_ALWAYS_EAGER", default=False)
CELERY_BROKER_URL = env.str("LARP_IN_UA_CELERY_BROKER", default="redis://redis:6380/1")
CELERY_RESULT_BACKEND = env.str("LARP_IN_UA_CELERY_RESULT_BACKEND", default="rpc://")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = DJANGO_TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'closest_lection_notifier': {
        'task': 'larp_in_ua.apps.scheduler.tasks.notify_closest_lection',
        'schedule': crontab(),
    },
    'closest_event_notifier': {
        'task': 'larp_in_ua.apps.scheduler.tasks.notify_closest_events',
        'schedule': crontab(),
    },
    'closest_night_event_notifier': {
        'task': 'larp_in_ua.apps.scheduler.tasks.notify_closest_night_event',
        'schedule': crontab(),
    },
    'refresh_hook': {
        'task': 'larp_in_ua.apps.common.tasks.refresh_hook',
        'schedule': crontab(
            minute='0',
            hour='*/6'
        ),
    },
    # 'heartbeat': {
    #     'task': 'larp_in_ua.apps.common.tasks.heartbeat',
    #     'schedule': crontab(minute="*/2"),
    # },
}
