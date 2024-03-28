from django import forms

from django.forms import TextInput, Textarea, NumberInput, Select, URLInput
from .models import Category, Comment

width1, width2 = 600, 120

class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=TextInput(attrs={"class":'form-control  mb-2',  'style': f'width:{width1}px;'}))
    img_url = forms.URLField(label="Image URL", required=False, widget=URLInput(attrs={"class":'form-control  mb-2', 'style': f'width:{width1}px;', 'placeholder': 'http://...'}))
    starting_price = forms.DecimalField(max_digits=7, decimal_places=2, min_value=1.00, initial="1.00 €", label="Price in EUR", widget=NumberInput(attrs={"class":'form-control mb-2', 'placeholder': '1.00 €',  'style': f'width:{width2}px; text-align: end;'}))
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={"class":'form-control  mb-2', 'style': f'width:{width2}px; text-align: center;' }))
    
    NEW, USED = "NEW", "USED"
    condition_choices = ((NEW, "new"), (USED, "used"))
    condition = forms.ChoiceField(choices=condition_choices, widget=Select(attrs={"class":'form-control  mb-2', 'style': f'width:{width2}px; text-align: center; text-align: center;' }))
    
    details = forms.CharField(required=False, widget=Textarea(attrs={"rows": "6", "class":'form-control',  'style': f'width:{width1}px;'}))


class CommentForm(forms.Form):
    title = forms.CharField(label="", required=False, widget=TextInput(attrs={"class":'form-control  mb-2', 'placeholder': "Comment title"}))
    content = forms.CharField(label="", required=True, widget=Textarea(attrs={"rows": "5", "class": "form-control mb-2",'placeholder': "Your comment"}))
    
    
class BidForm(forms.Form):
    price = forms.DecimalField(max_digits=7, min_value=1.00 , decimal_places=2, label="", widget=NumberInput(attrs={"class":'form-control mb-2', 'placeholder': 'Place Bid',  'style': f'width:{width2}px; text-align: end;'}))