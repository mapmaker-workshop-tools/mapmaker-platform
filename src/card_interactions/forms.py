from django import forms
from workshop.models import Card

CARD_TYPE_CHOICES =(
    ("1", "legend_1"),
    ("2", "legend_2"),
    ("3", "legend_3"),
    ("4", "legend_4"),
    ("5", "legend_5"),
    ("6", "image_card"),
)

tailwind_class = """w-full border-2 border-ch-gray-light
        bg-ch-gray-dark rounded-lg
        focus:outline-ch-green-light focus:outline-0
        focus:outline-offset-0 focus:border-2
        focus:border-woys-purple focus:shadow-none
        focus:ring-0 focus:shadow-0"
        """

comment_class = """w-full px-0 text-sm text-gray-900 bg-white border-0  focus:ring-0  """

class CardForm(forms.Form):
    cardtype = forms.ChoiceField(choices = CARD_TYPE_CHOICES, widget=forms.Select(attrs={"class": tailwind_class}))
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": tailwind_class}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": tailwind_class}))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["cardtype"].label = ""
        self.fields["title"].label = ""
        self.fields["description"].label = ""



class CardTitle(forms.Form):
    #cardtype = forms.ChoiceField(choices = CARD_TYPE_CHOICES, widget=forms.Select(attrs={"class": tailwind_class}))
    #title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": tailwind_class, "placeholder": "Write a new title", "label": ""}))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        

class imageCardTitle(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["image"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["image"].label = ""



class CardDescription(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={"class": tailwind_class, "placeholder": "Write a new description"}))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["description"].label = ""

class CardResource(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={"class": tailwind_class, "placeholder": "What is your resource about?"}))
    url = forms.CharField(widget=forms.TextInput(attrs={"class": tailwind_class, "placeholder": "What is the URL of your resource?"}))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["description"].label = ""
        self.fields["url"].label = ""

class CardComment(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={"class": comment_class, "placeholder":"type a comment"}))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["comment_text"].label = ""
