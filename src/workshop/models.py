from random import randrange

from django.db import models
from django.utils import timezone
from users.models import CustomUser
import random
from django.conf import settings
from zipfile import ZipFile
import shutil


# Create your models here.
class Workshop(models.Model):
    is_active = models.BooleanField(default=True)
    workshop_name = models.CharField(max_length=30, blank=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    workshop_date = models.DateTimeField()
    participants = models.ManyToManyField(CustomUser, related_name = "workshop_participants")
    workshop_owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name = "workshop_owners")
    card_order = models.TextField(null=True, blank=True)
    legend_label_1 = models.CharField(blank=False, max_length=40, default="Ambition")
    legend_hex_color_1 = models.CharField(blank=False, max_length=6, default="00000")
    legend_icon_1 = models.CharField(blank=False, max_length=40, default="flag-solid.svg")
    legend_label_2 = models.CharField(blank=False, max_length=40, default="Pro")
    legend_hex_color_2 = models.CharField(blank=False, max_length=6, default="51c1ff")
    legend_icon_2 = models.CharField(blank=False, max_length=40, default="thumbs-up-solid.svg")
    legend_label_3 = models.CharField(blank=False, max_length=40, default="Challenge")
    legend_hex_color_3 = models.CharField(blank=False, max_length=6, default="ffeb39")
    legend_icon_3 = models.CharField(blank=False, max_length=40, default="mountain-solid.svg")
    legend_label_4 = models.CharField(blank=False, max_length=40, default="Idea")
    legend_hex_color_4 = models.CharField(blank=False, max_length=6, default="E6799D")
    legend_icon_4 = models.CharField(blank=False, max_length=40, default="lightbulb-solid.svg")
    legend_label_5 = models.CharField(blank=False, max_length=40, default="Con")
    legend_hex_color_5 = models.CharField(blank=False, max_length=6, default="78E7BF")
    legend_icon_5 = models.CharField(blank=False, max_length=40, default="thumbs-down-solid.svg")

    # If we save a new Workshop (new because no primary key yet) we add 100 empty cards to database
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            for _ in range(308):
                card = Card(cardtype="empty",
                        author=CustomUser(pk=5),
                        workshop=Workshop.objects.latest("date_created"),
                        title=str(randrange(20000)),
                        description="")
                card.save()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.workshop_name

class Card(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    cardtypechoice = models.TextChoices("cardtype", "legend_1 legend_2 legend_3 legend_4 legend_5 image_card empty")
    cardtype = models.CharField(blank=False, choices=cardtypechoice.choices, max_length=20)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=False,related_name = "card_author")
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, related_name = "workshop")
    title = models.CharField(max_length=100, unique=False, blank=True)
    description = models.TextField(blank=True)
    followers = models.ManyToManyField(CustomUser, blank=True, related_name = "card_followers")
    image_Url = models.URLField(blank=True, default="https://www.grouphealth.ca/wp-content/uploads/2018/05/placeholder-image.png")
    image = models.FileField(upload_to="media/cardimages/", default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.workshop.workshop_name + " - " + self.title
    
    
class ImportImages(models.Model):
    zip_import = models.FileField(blank=True)
    workshop = models.ForeignKey(Workshop, blank=False, on_delete=models.CASCADE, related_name="workshop_images")
    
    def save(self, delete_zip_import=True, *args, **kwargs):
        super(ImportImages, self).save(*args, **kwargs)
        
        workshop = Workshop.objects.get(id=self.workshop.id)
        cards = Card.objects.filter(workshop=workshop, cardtype='empty')
        shutil.unpack_archive(self.zip_import, 'dir_out')
            
        """for i in cards:
            print(random.sample(cards, 3))"""