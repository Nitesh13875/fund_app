import pandas as pd
from django.http import HttpResponse
from mfapp.forms import UploadCSVForm
from mfapp.models import Fund, CSVData, Dt, StockDataRefresh ,Settings
from django.shortcuts import render, redirect
from datetime import datetime
from mfapp.forms1 import AccessTokenForm
import logging
from mfapp.models import Settings
import requests


def update_access_token(request):
    if request.method == 'POST':
        form = AccessTokenForm(request.POST)
        if form.is_valid():
            # Save the access token
            new_token = form.cleaned_data['access_token']
            Settings.objects.create(access_token=new_token)

            tokens = Settings.objects.all()
            if tokens.count() > 5:
                # Delete the oldest token
                tokens.order_by('created_at').first().delete()

            return redirect('update_access_token')  # Redirect to the same page after saving
    else:
        form = AccessTokenForm()

    # Pass existing tokens to the template
    tokens = Settings.objects.all()
    return render(request, 'update_access_token.html', {'form': form, 'tokens': tokens})
