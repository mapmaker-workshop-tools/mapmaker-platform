from django import forms
from .models import EmailList, Order


tailwind_class = """class="bg-gray-50 max-w-half border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"""
        

class EmailMarketing(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder':'email@email.com', 'label':''}))

    class Meta:
        model = EmailList
        fields = ("email")


class Orderform(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder':'email@email.com', 'label':''}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_class, 'placeholder': 'Tell us about what you would like to order and we will get back to you'}))

    class Meta:
        model = Order
        fields = ("email")
