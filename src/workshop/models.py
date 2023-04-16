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
    legend_label_1 = models.CharField(blank=False, max_length=40, default='legend_1')
    legend_hex_color_1 = models.CharField(blank=False, max_length=6, default='78E7BF')
    legend_icon_1 = models.CharField(blank=False, max_length=40, default='thumbs-up-solid.svg')
    legend_label_2 = models.CharField(blank=False, max_length=40, default='legend_2')
    legend_hex_color_2 = models.CharField(blank=False, max_length=6, default='51c1ff')
    legend_icon_2 = models.CharField(blank=False, max_length=40, default='thumbs-up-solid.svg')
    legend_label_3 = models.CharField(blank=False, max_length=40, default='legend_3')
    legend_hex_color_3 = models.CharField(blank=False, max_length=6, default='ffeb39')
    legend_icon_3 = models.CharField(blank=False, max_length=40, default='thumbs-up-solid.svg')
    legend_label_4 = models.CharField(blank=False, max_length=40, default='legend_4')
    legend_hex_color_4 = models.CharField(blank=False, max_length=6, default='E6799D')
    legend_icon_4 = models.CharField(blank=False, max_length=40, default='thumbs-up-solid.svg')
    legend_label_5 = models.CharField(blank=False, max_length=40, default='legend_5')
    legend_hex_color_5 = models.CharField(blank=False, max_length=6, default='000000')
    legend_icon_5 = models.CharField(blank=False, max_length=40, default='thumbs-up-solid.svg')
        
    # If we save a new Workshop (new because no primary key yet) we add 100 empty cards to database
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            for _ in range(308):
                card = Card(cardtype='empty',
                        author=CustomUser(pk=5),
                        workshop=Workshop.objects.latest('date_created'),
                        title=str(randrange(20000)),
                        description='')
                card.save()
            legend = Legenda(workshop=Workshop.objects.latest('date_created'))
            legend.save()
            
        return super().save(*args, **kwargs) 
        
    def __str__(self):
        return self.workshop_name

class Card(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    cardtypechoice = models.TextChoices('cardtype', 'legend_1 legend_2 legend_3 legend_4 legend_5 image_card empty')
    cardtype = models.CharField(blank=False, choices=cardtypechoice.choices, max_length=20)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False,related_name = 'card_author')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, related_name = 'workshop')
    title = models.CharField(max_length=100, unique=False, blank=False)
    description = models.TextField(blank=True,)
    followers = models.ManyToManyField(CustomUser, related_name = 'card_followers')
    image_Url = models.URLField(blank=True, default='https://www.grouphealth.ca/wp-content/uploads/2018/05/placeholder-image.png')
    
    def __str__(self):
        return self.workshop.workshop_name + ' - ' + self.title