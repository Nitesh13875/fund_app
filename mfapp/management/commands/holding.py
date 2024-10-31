import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mfapp.models import Fund, Portfolio, Holding, RiskVolatility, CSVData, Settings
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetch and store AMC, Fund, Portfolio, and Holdings data from Morningstar API'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the most recent access token
            latest_setting = Settings.objects.order_by('-created_at').first()
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
            self.fetch_portfolio_data(ids_list, self.ACCESS_TOKEN)  # Pass the access token here

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

    def fetch_portfolio_data(self, ids, access_token):
        for fund_id in ids:
            url = f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/holding/v2/{fund_id}/data?premiumNum=100&freeNum=25&hideesg=true&languageId=en&locale=en&clientId=RSIN_SAL&benchmarkId=mstarorcat&component=sal-mip-holdings&version=4.31.0&access_token={access_token}"
            response = self.fetch_data(url)
            if not response:
                continue

            data = response.json()
            portfolio_data = data.get("holdingSummary", {})
            holdings_data = data.get("equityHoldingPage", {}).get("holdingList", [])

            # Use a transaction to ensure atomic database operations
            with transaction.atomic():
                # Create or update Portfolio object
                portfolio, _ = Portfolio.objects.update_or_create(
                    master_portfolio_id=data.get("masterPortfolioId"),
                    defaults={
                        'sec_id': data.get("secId"),
                        'base_currency_id': data.get("baseCurrencyId"),
                        'domicile_country_id': data.get("domicileCountryId"),
                        'number_of_holding': data.get("numberOfHolding", 0),
                        'number_of_equity_holding': data.get("numberOfEquityHolding", 0),
                        'portfolio_date': pd.to_datetime(portfolio_data.get("portfolioDate"),
                                                         errors='coerce').date() if portfolio_data.get(
                            "portfolioDate") else None,
                        'top_holding_weighting': portfolio_data.get("topHoldingWeighting", 0.0),
                        'last_turnover': portfolio_data.get("lastTurnover", None),
                        'last_turnover_date': pd.to_datetime(portfolio_data.get("LastTurnoverDate"),
                                                             errors='coerce').date() if portfolio_data.get(
                            "LastTurnoverDate") else None,
                        'average_turnover_ratio': portfolio_data.get("averageTurnoverRatio", None),
                    }
                )

                for holding in holdings_data:
                    Holding.objects.update_or_create(
                        portfolio=portfolio,
                        sec_id=holding.get("secId"),  # Assuming sec_id is unique per holding
                        defaults={
                            'security_name': holding.get("securityName"),
                            'weighting': holding.get("weighting"),
                            'number_of_share': holding.get("numberOfShare", 0),
                            'market_value': holding.get("marketValue", 0.0),
                            'country': holding.get("country", ""),
                            'ticker': holding.get("ticker", ""),
                            'sector': holding.get("sector", ""),
                            'total_return_1_year': holding.get("totalReturn1Year", None),
                            'forward_pe_ratio': holding.get("forwardPERatio", None),
                            'stock_rating': holding.get("stockRating", None),
                            'assessment': holding.get("assessment", ""),
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"Stored data for Fund ID: {fund_id}"))
