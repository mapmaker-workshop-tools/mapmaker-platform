from django.contrib import admin

# Register your models here.
from .models import Workshop, Card


admin.autodiscover()


admin.site.register(Workshop)
admin.site.register(Card)