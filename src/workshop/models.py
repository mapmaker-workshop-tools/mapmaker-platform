from django.db import models
from users.models import CustomUser
from django.utils import timezone
from random import randrange
import uuid



# Create your models here.
class Workshop(models.Model):
    is_active = models.BooleanField(default=True)
    workshop_name = models.CharField(max_length=30, blank=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    workshop_date = models.DateTimeField()
    participants = models.ManyToManyField(CustomUser, related_name = 'workshop_participants')
    workshop_owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'workshop_owners')
    card_order = models.TextField(null=True, blank=True)
    
    # If we save a new Workshop (new because no primary key yet) we add 100 empty cards to database
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            for _ in range(500):
                print("Creating card")
                card = Card(cardtype='empty',
                        author=CustomUser(pk=5),
                        workshop=Workshop.objects.latest('date_created'),
                        title=str(randrange(20000)),
                        description='')
                card.save()
  
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.workshop_name

class Card(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    cardtypechoice = models.TextChoices('cardtype', 'ambition challenge idea pro con empty')
    cardtype = models.CharField(blank=False, choices=cardtypechoice.choices, max_length=20)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False,related_name = 'card_author')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, related_name = 'workshop')
    title = models.CharField(max_length=30, unique=False, blank=False)
    description = models.TextField(blank=True,)
    followers = models.ManyToManyField(CustomUser, related_name = 'card_followers')
    def __str__(self):
        return self.workshop.workshop_name + ' - ' + self.title

class Legenda(models.Model):
    legend_label = models.CharField(blank=False, max_length=40)
    legend_color = models.CharField(blank=False, max_length=40)
    legend_icon = models.CharField(blank=False, max_length=40)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, related_name = 'workshoplegenda')