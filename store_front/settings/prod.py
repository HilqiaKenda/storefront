from .common import *
import dj_database_url
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

"8df-mheiuw-@(4s3oe26=cfa5v+51pvqo2(g44oex=9o#y@_^v"
ALLOWED_HOSTS = ["groot-buy-prod-09bd3e62e79c.herokuapp.com"]

DATABASES = {
    'default': dj_database_url.config()
    }
READIS_URL = os.environ.get('CACHETOGO_TLS_URL')

CELERY_BROKER_URL = READIS_URL


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": READIS_URL,
        'TIMEOUT': 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD =''
EMAL_PORT = os.environ['MAILGUN_SMTP_PORT']
DEFAULT_FROM_EMAIL = 'info@grootbuy.com'


LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "handlers": {
        'console': {
            'class': 'logging.StreamHandler',
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
        },
    },
    "loggers": {
        "": {
            "level": os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            "handlers": ["console", "file"],
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'  # string.format()
        }
    }
}   