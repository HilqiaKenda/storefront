from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECUfITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&&e#r7*w+6yjgp!dx=2(u!53_fc)r0o)l@$h@cy#pldqggy4_r'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAL_PORT = 2525


CELERY_BROKER_URL = 'redis://localhost:6379/1'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Groot5'
    }
}
