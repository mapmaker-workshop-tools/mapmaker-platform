from random import randrange

from core.settings import BASE_DIR
from core.utils import mp
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from thumbnails.fields import ImageField


from .managers import CustomUserManager


# Created using: https://testdriven.io/blog/django-custom-user-model/


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(default=timezone.now, editable=True)
    linkedin = models.CharField(max_length=300, unique=False, blank=True)
    organisation = models.CharField(max_length=100, unique=False, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    active_workshop = models.ForeignKey("workshop.Workshop", on_delete=models.SET("none"), blank=True, null=True)
    zoom_level = models.CharField(max_length=1, blank=True, default=0)
    avatar = ImageField(upload_to="media/avatars/", null=True, blank=True, pregenerated_sizes=["small", "medium", "large"])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        mp.people_set(self.email, {
            "$first_name"    : self.first_name,
            "$last_name"     : self.last_name,
            "$email"         : self.email,
            "$organisation"  : self.organisation,
            "$created"       : self.date_created,
            }, meta = {"$ignore_time" : True, "$ip" : 0})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
