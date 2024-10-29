from django import forms

class FundSearchForm(forms.Form):
    query = forms.CharField(label='Search by Scheme ID, ISIN, Scheme Name, or Scheme Code', max_length=255)
