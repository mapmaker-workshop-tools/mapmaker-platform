from django.contrib import admin

# Register your models here.
from .models import Comment, Follower, Resource


class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment_text", "card", "author", "date_modified")
    list_filter = ("author", "date_created", "date_modified")
    search_fields = ["comment_text"]

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("user_like", "card_liked")
    list_filter = ("user_like", "card_liked")
    search_fields = ["card_liked"]

class ResourceAdmin(admin.ModelAdmin):
    list_display = ("document_description", "card", "owner", "date_modified")
    list_filter = ("owner", "date_created", "date_modified")
    search_fields = ["document_description"]

admin.site.register(Comment, CommentAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Resource, ResourceAdmin)


