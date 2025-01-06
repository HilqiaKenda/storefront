from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECUfITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&&e#r7*w+6yjgp!dx=2(u!53_fc)r0o)l@$h@cy#pldqggy4_r'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Groot'
    }
}
