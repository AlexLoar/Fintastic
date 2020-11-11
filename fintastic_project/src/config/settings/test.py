from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="iq8IaIwiuIEK37Pfr6rzIpRB6eEs6HqLIhfPcqPVADuAyCChaI5ZZpWO6It5npVi")
# https://docs.djangoproject.com/en/3.1/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
# https://docs.djangoproject.com/en/3.1/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/3.1/ref/settings/#email-port
EMAIL_PORT = 1025

