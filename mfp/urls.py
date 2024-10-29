from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mfapp.urls')),  # This includes fundapp's URLs in the project
]
