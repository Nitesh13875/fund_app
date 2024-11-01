from django.urls import path
from .views import home
from .Features.Fund_nav_chart import fund_dashboard
from .Features.Upload_csv import process_csv_upload
from .Features.Update_access_token import update_access_token

urlpatterns = [
    path('', home, name='home'),
    path('process_csv_upload/', process_csv_upload, name='process_csv_upload'), # Home page that shows the dashboard
    path('update_access_token/', update_access_token, name='update_access_token'),
    path('fund_dashboard/',fund_dashboard, name='fund_dashboard'),

]
