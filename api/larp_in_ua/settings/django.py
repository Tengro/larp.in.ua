import os

from .environment import env


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(*path):
    return os.path.join(BASE_DIR, *path)


DEBUG = env.bool("LARP_IN_UA_DEBUG", default=False)

INTERNAL_IPS = env.list("LARP_IN_UA_INTERNAL_IPS", default=[])

ALLOWED_HOSTS = env.list("LARP_IN_UA_ALLOWED_HOSTS", default=[])

SECRET_KEY = env.str("LARP_IN_UA_SECRET_KEY")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + "/../logfile",
        },
    },
    'root': {
        'handlers': ['console', 'logfile'],
        'level': 'INFO',
    },
}


INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "rest_framework",
    "django_extensions",
    "django_filters",
    "drf_yasg",
    "django_telegrambot",
    # our apps
    "larp_in_ua.apps.common.apps.CommonConfig",
    "larp_in_ua.apps.accounts.apps.AccountConfig",
    "larp_in_ua.apps.scheduler.apps.SchedulerConfig",
] + env.list("LARP_IN_UA_DEV_INSTALLED_APPS", default=[])

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
] + env.list("LARP_IN_UA_DEV_MIDDLEWARE", default=[])

ROOT_URLCONF = "larp_in_ua.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [rel("templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "larp_in_ua.wsgi.application"

DATABASES = {"default": env.db("LARP_IN_UA_DATABASE_URL", default="psql://postgres:GanzaUnion1@database:5433/larp_in_ua_db")}

AUTH_USER_MODEL = "accounts.UserAccount"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SECURE_BROWSER_XSS_FILTER = env.bool("LARP_IN_UA_SECURE_BROWSER_XSS_FILTER", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("LARP_IN_UA_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SESSION_COOKIE_HTTPONLY = env.bool("LARP_IN_UA_SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_SECURE = env.bool("LARP_IN_UA_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("LARP_IN_UA_CSRF_COOKIE_SECURE", default=True)
X_FRAME_OPTIONS = env.str("LARP_IN_UA_X_FRAME_OPTIONS", default="SAMEORIGIN")
SECURE_HSTS_SECONDS = env.int("LARP_IN_UA_SECURE_HSTS_SECONDS", default=31536000)  # 1 year
SESSION_COOKIE_NAME = "s"
CSRF_COOKIE_NAME = "c"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Kiev"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (rel("..", "..", "api", "locale"),)

STATIC_URL = env.str("LARP_IN_UA_STATIC_URL", default="/s/")
STATIC_ROOT = env.str("LARP_IN_UA_STATIC_ROOT", default=rel("..", "..", "public", "static"))

MEDIA_URL = env.str("LARP_IN_UA_MEDIA_URL", default="/m/")
MEDIA_ROOT = env.str("LARP_IN_UA_MEDIA_ROOT", rel("..", "..", "public", "media"))
FILE_UPLOAD_PERMISSIONS = 0o644

EMAIL_BACKEND = env.str("LARP_IN_UA_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":  # pragma: no cover
    EMAIL_HOST = env.str("LARP_IN_UA_EMAIL_HOST")
    EMAIL_PORT = env.str("LARP_IN_UA_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("LARP_IN_UA_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("LARP_IN_UA_EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env.bool("LARP_IN_UA_EMAIL_USE_TLS", default=True)

SITE_ID = env.int("SITE_ID", default=1)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

APPEND_SLASH = True
