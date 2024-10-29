from . import views
from django.contrib import admin
from django.urls import path, include

from django.urls import path
from mfapp.Features.fund_search import fund_dashboard

urlpatterns = [
    path('', fund_dashboard, name='fund_dashboard'),
]
