from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY')
# https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
