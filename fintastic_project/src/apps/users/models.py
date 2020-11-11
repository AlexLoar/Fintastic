from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=150, blank=True)
    password = models.CharField(_('Password'), max_length=128, blank=True)
    name = models.CharField(_('Name'), max_length=128)
    email = models.EmailField(_('Email address'), unique=True)
    age = models.PositiveSmallIntegerField(_('Age'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']
