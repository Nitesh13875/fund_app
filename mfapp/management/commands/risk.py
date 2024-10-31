import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mfapp.models import Holding, RiskVolatility, CSVData, Settings
import time


class Command(BaseCommand):
    help = 'Fetch and store AMC, Fund, Portfolio, and Holdings data from Morningstar API'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the most recent access token
            latest_setting = Settings.objects.order_by('-created_at').first()
            if not latest_setting:
                self.stdout.write(self.style.ERROR('Access token not set.'))
                return

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
            self.fetch_and_save_risk_volatility(ids_list)

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

    def fetch_and_save_risk_volatility(self, ids):
        for fund_id in ids:
            url = (f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskVolatility/{fund_id}/data?"
                   f"currency=&longestTenure=false&languageId=en&locale=en&clientId=RSIN_SAL&"
                   f"benchmarkId=mstarorcat&component=sal-mip-risk-volatility-measures&version=4.13.0&"
                   f"access_token={self.ACCESS_TOKEN}")

            response = self.fetch_data(url)
            if not response:
                continue

            try:
                data = response.json()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"JSON decode error for Fund ID {fund_id}: {e}"))
                continue

            fund_risk_volatility = data.get("fundRiskVolatility", {})
            category_risk_volatility = data.get("categoryRiskVolatility", {})
            timeframes = ["for1Year", "for3Year", "for5Year"]

            # Prepare to store all fund data
            all_defaults = {
                'index_name': data.get('indexName'),
                'fund_name': data.get('fundName'),
                'category_name': data.get('categoryName'),
            }

            with transaction.atomic():
                for timeframe in timeframes:
                    fund_data = fund_risk_volatility.get(timeframe, {})
                    category_data = category_risk_volatility.get(timeframe, {})
                    defaults = {
                        f"fund_alpha_{timeframe[3]}y": fund_data.get("alpha"),
                        f"fund_beta_{timeframe[3]}y": fund_data.get("beta"),
                        f"fund_r_squared_{timeframe[3]}y": fund_data.get("rSquared"),
                        f"fund_std_dev_{timeframe[3]}y": fund_data.get("standardDeviation"),
                        f"fund_sharpe_{timeframe[3]}y": fund_data.get("sharpeRatio"),
                        f"category_alpha_{timeframe[3]}y": category_data.get("alpha"),
                        f"category_beta_{timeframe[3]}y": category_data.get("beta"),
                        f"category_r_squared_{timeframe[3]}y": category_data.get("rSquared"),
                        f"category_std_dev_{timeframe[3]}y": category_data.get("standardDeviation"),
                        f"category_sharpe_{timeframe[3]}y": category_data.get("sharpeRatio"),
                    }

                    # Add to defaults to include timeframe data
                    all_defaults.update(defaults)

                # Create or update RiskVolatility entry
                RiskVolatility.objects.update_or_create(
                    fund_id=fund_id,
                    defaults=all_defaults
                )

                self.stdout.write(self.style.SUCCESS(f"Stored data for Fund ID: {fund_id}"))
            time.sleep(1)  # Delay between API calls
