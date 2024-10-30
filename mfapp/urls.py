from django.urls import path
from .views import process_csv_upload,update_access_token,home
from .Features.fund_search import fund_dashboard
from .views import run_command

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('process_csv_upload/', process_csv_upload, name='process_csv_upload'), # Home page that shows the dashboard
    path('update_access_token/', update_access_token, name='update_access_token'),
    path('fund_dashboard/',fund_dashboard, name='fund_dashboard'),
    path('run-command/<str:command>/', run_command, name='run_command'),

]
