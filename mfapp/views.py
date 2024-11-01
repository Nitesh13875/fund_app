import pandas as pd
from django.http import HttpResponse
from .forms import UploadCSVForm
from .models import Fund, CSVData, Dt, StockDataRefresh ,Settings
from django.shortcuts import render, redirect
from datetime import datetime
from .forms1 import AccessTokenForm
import logging
from django.shortcuts import render, redirect
from .models import Settings
import requests

def home(request):
    return render(request, 'home.html')


