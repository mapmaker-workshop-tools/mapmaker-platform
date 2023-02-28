from django.contrib import admin


# Register your models here.
from .models import Comment, Like, Document


admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Document)
