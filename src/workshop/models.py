from django.db import models
from users.models import CustomUser
from django.utils import timezone


# Create your models here.
class Workshop(models.Model):
    is_active = models.BooleanField(default=True)
    workshop_name = models.CharField(max_length=30, unique=True, blank=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    workshop_date = models.DateTimeField()
    participants = models.ManyToManyField(CustomUser, related_name = 'workshop_participants')
    workshop_owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'workshop_owners')
        
    def __str__(self):
        return self.workshop_name

class Card(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    cardtypechoice = models.TextChoices('cardtype', 'ambition challenge idea pro con')
    cardtype = models.CharField(blank=False, choices=cardtypechoice.choices, max_length=20)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False,related_name = 'card_author')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, related_name = 'workshop')
    title = models.CharField(max_length=30, unique=True, blank=False)
    description = models.TextField(blank=True,)
    parentnode = models.CharField(max_length=30, unique=False, blank=True)
    followers = models.ManyToManyField(CustomUser, related_name = 'card_followers')
    
    def __str__(self):
        return self.title

    
    


    