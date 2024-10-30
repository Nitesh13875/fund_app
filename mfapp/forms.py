from django import forms
from django import forms
from .models import Settings

class FundSearchForm(forms.Form):
    query = forms.CharField(label='Search by Scheme ID, ISIN, Scheme Name, or Scheme Code', max_length=255)

class UploadCSVForm(forms.Form):
    file = forms.FileField()

class AccessTokenForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['access_token']