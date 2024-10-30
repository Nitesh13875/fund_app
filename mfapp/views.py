import pandas as pd
from django.http import HttpResponse
from .forms import UploadCSVForm
from .models import Fund, CSVData, Dt, StockDataRefresh ,Settings
from django.shortcuts import render, redirect
from datetime import datetime
from .forms1 import AccessTokenForm

from django.shortcuts import render, redirect
from .models import Settings
import requests

def home(request):
    return render(request, 'home.html')

def process_csv_upload(request):
    last_refresh_time = "Never"
    last_refresh_entries = StockDataRefresh.objects.order_by('-last_refresh_time')
    if last_refresh_entries.count() > 5:
        excess_entries = last_refresh_entries[5:]
        excess_entries.delete()
    last_refresh = StockDataRefresh.objects.order_by('-last_refresh_time').first()

    if last_refresh:
        last_refresh_time = last_refresh.last_refresh_time


    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            df = pd.read_csv(uploaded_file)

            # Check if 'isin' or 'ISIN' column exists (case insensitive)
            if 'isin' not in df.columns.str.lower().tolist():
                return HttpResponse("Error: CSV must contain an 'isin' column.", status=400)

            output_data = []
            for _, row in df.iterrows():
                isin = row['isin']

                fund = Fund.objects.filter(isin=isin).first()
                csv_data = CSVData.objects.filter(isin=isin).first()
                dt = Dt.objects.filter(scheme_id=csv_data.scheme_id if csv_data else None).first()

                row_data = {
                    "isin": isin,
                    "scheme_name": csv_data.scheme_name if csv_data else None,
                    'inception_date': fund.inceptionDate if fund else None,
                    "prospectus_benchmark_name": fund.prospectus_benchmark_name if fund else None,
                    "last_turnover_ratio": fund.last_turnover_ratio if fund else None,
                    "equity_style_box": fund.equity_style_box if fund else None,
                    "total_asset": fund.total_asset if fund else None,
                    "one_month_return": dt.one_month_return if dt else None,
                    "six_month_return": dt.six_month_return if dt else None,
                    "one_year_return": dt.one_year_return if dt else None,
                    "three_year_return": dt.three_year_return if dt else None,
                    "five_year_return": dt.five_year_return if dt else None,
                    "investment_name": fund.investment_name if fund else None,
                    "expense_ratio": fund.expense_ratio if fund else None,
                }
                output_data.append(row_data)

            # Convert to DataFrame for easy CSV export
            output_df = pd.DataFrame(output_data)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=processed_data.csv'
            output_df.to_csv(path_or_buf=response, index=False)
            return response

    form = UploadCSVForm()
    current_year = datetime.now().year
    return render(request, 'dashboard.html', {
        'form': form,
        'current_year': current_year,
        'last_refresh_time': last_refresh_time,
    })





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
    return render(request, r'C:\Users\nites\Desktop\MF\mfp\mfapp\templates\update_access_token.html', {'form': form, 'tokens': tokens})

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import logging
import socket

logger = logging.getLogger(__name__)

@csrf_exempt  # This should only be used if you are certain you need it
def run_command(request, command):
    if request.method == 'POST':
        try:
            # Call the management command
            call_command(command)
            output = f"{command} executed successfully."
            logger.info(output)
            return JsonResponse({'output': output})
        except Exception as e:
            logger.error(f"Error running command {command}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
