from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.utils import mp

from django.db import models

# Create your models here.
class EmailList(Model):
    email = models.EmailField(_("email address"))
    date_created = models.DateTimeField(default=timezone.now, editable=False)