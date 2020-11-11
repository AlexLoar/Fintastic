"""config URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _

from config.router import urlpatterns as api_urlpatterns


# Admin URLs
admin.site.site_header = _('Fintastic Project')
urlpatterns = [
    path(r'admin/', admin.site.urls),
]

# API URLs
urlpatterns += [
    path('api/v1/', include(api_urlpatterns)),
]
