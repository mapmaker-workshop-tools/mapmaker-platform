from django import forms
from .models import EmailList


tailwind_class = """class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5     dark:focus:ring-blue-500 dark:focus:border-blue-500"""
        
comment_class = """w-full px-0 text-sm text-gray-900 bg-white border-0  focus:ring-0  """

class EmailMarketing(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder':'email@email.com', 'label':''}))

    class Meta:
        model = EmailList
        fields = ("email")
