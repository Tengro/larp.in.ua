from datetime import timedelta

from .environment import env


LARP_IN_UA_FEATURES = env.list("LARP_IN_UA_FEATURES", default=[])

LARP_IN_UA_EMAIL_FROM = env.str("LARP_IN_UA_EMAIL_FROM", default="no-reply@example.com")

LARP_IN_UA_AUTH_COOKIE_NAME = env.str("LARP_IN_UA_AUTH_COOKIE_NAME", default="a")

# Reset password link lifetime interval (in seconds). By default: 1 hour.
LARP_IN_UA_RESET_PASSWORD_EXPIRATION_DELTA = timedelta(seconds=env.int("LARP_IN_UA_RESET_PASSWORD_EXPIRATION_DELTA", default=3600))

if "LOG_SQL" in LARP_IN_UA_FEATURES:  # pragma: no cover
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
        "formatters": {
            "simple": {"format": "[%(asctime)s] %(levelname)s %(message)s"},
            "verbose": {"format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"},
            "sql": {"()": "larp_in_ua.loggers.SQLFormatter", "format": "[%(duration).3f] %(statement)s"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "verbose", "level": "DEBUG"},
            "sql": {"class": "logging.StreamHandler", "formatter": "sql", "level": "DEBUG"},
        },
        "loggers": {
            "django.db.backends": {
                "handlers": ["sql"],
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "propagate": False,
            },
            "django.db.backends.schema": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        },
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


DJANGO_TELEGRAMBOT = {

    'STRICT_INIT': True,
    'MODE': env.str("LARP_IN_UA_BOT_MODE", default='POLLING'),

    'WEBHOOK_SITE': 'https://tengro.site',
    'WEBHOOK_PREFIX': '/bot',
    'BOTS': [
        {
           'TOKEN': env.str("LARP_IN_UA_BOT_KEY"), #Your bot token.
           'MESSAGEQUEUE_ENABLED': True,
        },
    ],

}

TELEGRAM_WEBHOOK_SITE = 'https://tengro.site'
TELEGRAM_WEBHOOK_BASE = '/bot'
