from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models

# Create your models here.
class EmailList(models.Model):
    email = models.EmailField(_("email address"))
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.email