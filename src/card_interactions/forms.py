from django import forms


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
        
comment_class = """w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"""

class CardForm(forms.Form):
    cardtype = forms.ChoiceField(choices = CARD_TYPE_CHOICES, widget=forms.Select(attrs={'class': tailwind_class}))
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_class}))
    
class CardTitle(forms.Form):
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'Write a new title'}))
    
class CardDescription(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_class, 'placeholder': 'Write a new description'}))
    
class CardResource(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'What is your resource about?'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class, 'placeholder': 'What is the URL of your resource?'}))
    
class CardComment(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class': comment_class, 'placeholder':'type a comment'}))
    
    