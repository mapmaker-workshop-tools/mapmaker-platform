from django.contrib import admin

# Register your models here.
from django.contrib import admin


# Register your models here.
from .models import EmailList, Order


admin.site.register(EmailList)
admin.site.register(Order)
