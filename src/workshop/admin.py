from django.contrib import admin

# Register your models here.
from .models import Workshop, Card


admin.autodiscover()



class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('workshop_name', 'workshop_date', 'workshop_owner')
    list_filter = ('participants', 'workshop_date', 'workshop_owner')
    search_fields = ["workshop_name"]

class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'workshop', 'author', 'cardtype')
    list_filter = ('workshop', 'author', 'cardtype')
    search_fields = ['title']




admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Card, CardAdmin)
