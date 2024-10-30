from django import forms
from .models import Settings


from django import forms

class AccessTokenForm(forms.Form):
    access_token = forms.CharField(max_length=255, label="access_token")