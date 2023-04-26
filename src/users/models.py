from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from random import randrange
from core.utils import mp
from core.settings import BASE_DIR
from .managers import CustomUserManager


avatar_path = BASE_DIR / 'staticfiles/images/avatar.jpg'

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
    avatar_url = models.CharField(max_length=500, blank=True, default="https://api.dicebear.com/5.x/pixel-art/svg?seed="+str(randrange(1000)))
    active_workshop = models.ForeignKey('workshop.Workshop', on_delete=models.SET('none'), blank=True, null=True)
    zoom_level = models.CharField(max_length=1, blank=True, default=0)
    avatar = models.FileField(upload_to='media/avatars/', default=avatar_path, null=True, blank=True)
     
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        
        mp.people_set(self.email, {
            '$first_name'    : self.first_name,
            '$last_name'     : self.last_name,
            '$email'         : self.email,
            '$organisation'  : self.organisation,
            '$created'       : self.date_created,
            }, meta = {'$ignore_time' : True, '$ip' : 0})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email