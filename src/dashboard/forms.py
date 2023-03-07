from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from workshop.models import Card

CARD_TYPE_CHOICES =(
    ("1", "ambition"),
    ("2", "challenge"),
    ("3", "pro"),
    ("4", "con"),
    ("5", "idea"),
)

tailwind_class = """w-full border-2 border-ch-gray-light 
        bg-ch-gray-dark rounded-lg 
        focus:outline-ch-green-light focus:outline-0 
        focus:outline-offset-0 focus:border-2 
        focus:border-woys-purple focus:shadow-none 
        focus:ring-0 focus:shadow-0"
        """

class CardForm(forms.Form):
    cardtype = forms.ChoiceField(choices = CARD_TYPE_CHOICES, widget=forms.Select(attrs={'class': tailwind_class}))
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_class}))
    
class CardTitle(forms.Form):
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))