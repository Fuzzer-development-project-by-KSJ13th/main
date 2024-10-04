# forms.py
from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='제품 이름', max_length=100)
