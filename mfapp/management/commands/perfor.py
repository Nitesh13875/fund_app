import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mfapp.models import Fund, Portfolio, Holding, RiskVolatility, CSVData, Settings  # Make sure to import AccessToken
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    help = 'Fetch and store AMC, Fund, Portfolio, and Holdings data from Morningstar API'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the most recent access token
            latest_setting = Settings.objects.order_by('-created_at').first()  # Corrected fetching logic
            if not latest_setting:
                self.stdout.write(self.style.ERROR('Access token not set.'))
                return

            # Store the access token
            self.ACCESS_TOKEN = latest_setting.access_token

            # Fetch IDs from CSVData
            try:
                csv_data_objects = CSVData.objects.all()
                ids_list = [obj.scheme_id for obj in csv_data_objects if obj.scheme_id is not None]
                if not ids_list:
                    self.stdout.write(self.style.ERROR('No scheme IDs found in CSVData.'))
                    return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to read CSVData: {str(e)}"))
                return

            # Fetch and save risk volatility for the collected IDs
            self.fetch_fund_data(ids_list)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in handle method: {str(e)}"))

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
            return None
            
def fetch_fund_data(self, ids):
    for fund_id in ids:
        url = f"https://api-global.morningstar.com/sal-service/v1/fund/quote/v4/{fund_id}/data?fundServCode=&showAnalystRatingChinaFund=false&showAnalystRating=false&languageId=en&locale=en&clientId=RSIN_SAL&benchmarkId=mstarorcat&component=sal-mip-quote&version=4.13.0&access_token={self.ACCESS_TOKEN}"
        response = self.fetch_data(url)
        if not response:
            continue

        fund_data = response.json()
        sec_id = fund_data.get("secId")
        fund_defaults = {
            "isin": fund_data.get("isin"),
            "investment_name": fund_data.get("investmentName"),
            "inceptionDate": pd.to_datetime(fund_data.get("inceptionDate")).date() if fund_data.get("inceptionDate") else None,
            "prospectus_benchmark_name": fund_data.get("prospectusBenchmarkName"),
            "expense_ratio": float(fund_data.get("expenseRatio")) if fund_data.get("expenseRatio") not in [None, 'NA', ''] else None,
            "last_turnover_ratio": float(fund_data.get("lastTurnoverRatio")) if fund_data.get("lastTurnoverRatio") not in [None, 'NA', ''] else None,
            "equity_style_box": fund_data.get("equityStyleBox"),
            "expense": float(fund_data.get("expense")) if fund_data.get("expense") not in [None, 'NA', ''] else None,
            "morningstar_rating": int(fund_data.get("morningstarRating")) if fund_data.get("morningstarRating") not in [None, 'NA', ''] else None,
            "total_asset": float(fund_data.get("totalAsset")) if fund_data.get("totalAsset") not in [None, 'NA', ''] else None,
        }

        Fund.objects.update_or_create(sec_id=sec_id, defaults=fund_defaults)
        self.stdout.write(self.style.SUCCESS(f"Stored data for Fund ID: {fund_id}"))
