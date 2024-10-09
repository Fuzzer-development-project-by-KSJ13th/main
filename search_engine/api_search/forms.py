# forms.py
from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='Product Name', max_length=100)

    SEARCH_CHOICES = [
        ('shodan', 'shodan'),
        ('nvd', 'nvd')
    ]
    
    search_option = forms.ChoiceField(
        choices=SEARCH_CHOICES,  
        widget=forms.RadioSelect,  
        label="Select a search option",  # 라벨
    )