from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class EmailList(models.Model):
    email = models.EmailField(_("email address"))
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    contacted_lead = models.BooleanField(default=False)
    notes = models.TextField()

    def __str__(self):
        return self.email
    
# Create your models here.
class Order(models.Model):
    email = models.EmailField(_("email address"))
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    internalnotes = models.TextField()
    description = models.TextField()
    contacted_lead = models.BooleanField(default=False)


    def __str__(self):
        return self.email