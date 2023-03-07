from django.contrib import admin


# Register your models here.
from .models import Comment, Follower, Resource


admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(Resource)
