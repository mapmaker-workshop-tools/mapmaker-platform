from django import forms
from .models import EmailList


tailwind_class = """w-full border-2 border-ch-gray-light 
        bg-ch-gray-dark rounded-lg 
        focus:outline-ch-green-light focus:outline-0 
        focus:outline-offset-0 focus:border-2 
        focus:border-woys-purple focus:shadow-none 
        focus:ring-0 focus:shadow-0"
        """
        
comment_class = """w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"""

class EmailMarketing(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))

    class Meta:
        model = EmailList
        fields = ("email")
