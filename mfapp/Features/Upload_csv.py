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



def process_csv_upload(request):
    last_refresh_time = "Never"
    last_refresh_entries = StockDataRefresh.objects.order_by('-last_refresh_time')

    # Check if there are more than 5 entries and delete the excess without using offset directly
    if last_refresh_entries.count() > 5:
        excess_entries = list(last_refresh_entries[5:])
        for entry in excess_entries:
            entry.delete()

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
    return render(request, 'access_token.html', {
        'form': form,
        'current_year': current_year,
        'last_refresh_time': last_refresh_time,
    })