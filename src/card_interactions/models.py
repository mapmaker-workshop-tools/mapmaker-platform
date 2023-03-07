from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from workshop.models import Card


# Create your models here.
class Follower(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    user_like = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name = 'user_like')
    card_liked = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name = 'liked_card')
    
    def __str__(self):
        return str(self.id) +" - "+ self.card_liked.title +" From user " + self.user_like.first_name

class Comment(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name = 'comment_author')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name = 'commented_card')
    comment_text = models.TextField(unique=False, blank=True)    
    
    def __str__(self):
        return self.comment_text +" - "+ self.card.title
    
class Resource(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    documenttypechoices = models.TextChoices('documenttype', 'link document')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name = 'document_owner')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name = 'document_card')
    document_description = models.TextField(blank=False)    
    document_type = models.CharField(blank=False, choices=documenttypechoices.choices, max_length=20)
    document_url = models.CharField(max_length=500, unique=False, blank=False)

    
    def __str__(self):
        return self.document_description +" - "+ self.document_url

    