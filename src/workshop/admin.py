from django.contrib import admin

# Register your models here.
from .models import Workshop, Card, Legenda


admin.autodiscover()


admin.site.register(Workshop)
admin.site.register(Card)
admin.site.register(Legenda)
