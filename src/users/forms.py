from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser

tailwind_class = """w-full border-2 border-ch-gray-light 
        bg-ch-gray-dark rounded-lg 
        focus:outline-ch-green-light focus:outline-0 
        focus:outline-offset-0 focus:border-2 
        focus:border-woys-purple focus:shadow-none 
        focus:ring-0 focus:shadow-0"""

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserRegisterToWorkshop(forms.Form):
    
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}))
    organisation = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    class Meta:
            model = CustomUser



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
        
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}))
    
    
    class Meta:
            model = CustomUser
            fields = ("email","password")


class CustomUserProfile(UserChangeForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}))
    
    class Meta:
            model = CustomUser
            fields = ("username","password")
    