import csv
from django.core.management.base import BaseCommand
from mfapp.models import Dt, CSVData, StockDataRefresh  # Ensure CSVData is imported
import requests
from datetime import datetime, timedelta
import logging
import time

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    help = 'Load data from data.csv into Dt model and calculate returns'

    def fetch_nav_history(self, scheme_code):
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)  # Set a timeout for the request
                response.raise_for_status()  # Raise an error for HTTP errors
                data = response.json().get('data', [])
                if not data:
                    logging.warning(f"No NAV data returned for scheme code: {scheme_code}")
                return data
            except requests.exceptions.ChunkedEncodingError:
                logging.warning("ChunkedEncodingError: Response ended prematurely. Retrying...")
                time.sleep(2)  # Wait before retrying
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                break  # Exit the loop if a non-retryable error occurs
        return None

    def get_closest_nav(self, nav_data, target_date):
        nav_data_sorted = sorted(nav_data, key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse=True)
        for entry in nav_data_sorted:
            nav_date = datetime.strptime(entry['date'], '%d-%m-%Y')
            if nav_date <= target_date:
                return float(entry['nav'])
        return None

    def calculate_returns(self, nav_data):
        today = datetime.today()
        periods = {
            '1_month': today - timedelta(days=22),
            '6_month': today - timedelta(days=182),
            '1_year': today - timedelta(days=365),
            '3_year': today - timedelta(days=365 * 3),
            '5_year': today - timedelta(days=365 * 5)
        }
        required_days = {
            '1_month': 20, '6_month': 120,
            '1_year': 200, '3_year': 900, '5_year': 1700
        }

        nav_today = float(nav_data[0]['nav'])
        returns = {}
        trading_days = len(nav_data)

        for period, date in periods.items():
            if trading_days < required_days[period]:
                returns[period] = None
                continue
            nav_past = self.get_closest_nav(nav_data, date)
            if nav_past:
                returns[period] = round(((nav_today / nav_past) - 1) * 100, 2)
            else:
                returns[period] = None

        return (
            returns.get('1_month'), returns.get('6_month'),
            returns.get('1_year'), returns.get('3_year'), returns.get('5_year')
        )

    def handle(self, *args, **kwargs):
        csv_data_objects = CSVData.objects.all()
        for obj in csv_data_objects:
            scheme_code = obj.scheme_code
            nav_data = self.fetch_nav_history(scheme_code)

            if nav_data:
                one_month_return, six_month_return, one_year_return, three_year_return, five_year_return = self.calculate_returns(
                    nav_data)
            else:
                one_month_return = six_month_return = one_year_return = three_year_return = five_year_return = None

            Dt.objects.update_or_create(
                scheme_id=obj.scheme_id,
                defaults={
                    'one_month_return': one_month_return,
                    'six_month_return': six_month_return,
                    'one_year_return': one_year_return,
                    'three_year_return': three_year_return,
                    'five_year_return': five_year_return
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Stored data for scheme code: {scheme_code}"))

        # Log the stock data refresh
        StockDataRefresh.objects.create()
        self.stdout.write(self.style.SUCCESS("Stock data refresh record created."))
