from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# Created using: https://testdriven.io/blog/django-custom-user-model/


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(default=timezone.now, editable=True)
    linkedin = models.CharField(max_length=100, unique=False, blank=True)
    organisation = models.CharField(max_length=100, unique=False, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=100, blank=True, default="https://t4.ftcdn.net/jpg/03/59/58/91/360_F_359589186_JDLl8dIWoBNf1iqEkHxhUeeOulx0wOC5.jpg")
    organisation = models.CharField(max_length=100, blank=True)
    active_workshop = models.ForeignKey('workshop.Workshop', on_delete=models.SET('none'), blank=True, null=True)
    zoom_level = models.CharField(max_length=1, blank=True, default=0)
    



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email