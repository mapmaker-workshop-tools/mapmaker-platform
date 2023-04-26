from django.contrib import admin

# Register your models here.
from .models import EmailList, Order

class EmailListAdmin(admin.ModelAdmin):
    list_display = ('email', 'contacted_lead', 'date_created')
    list_filter = ('email', 'contacted_lead', 'date_created')
    search_fields = ['email']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'contacted_lead', 'date_created')
    list_filter = ('email', 'contacted_lead', 'date_created')
    search_fields = ['email']


admin.site.register(EmailList, EmailListAdmin)
admin.site.register(Order, OrderAdmin)
