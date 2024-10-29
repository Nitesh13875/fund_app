import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mfapp.models import Fund, Portfolio, Holding,RiskVolatility # Ensure the import path is correct
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    help = 'Fetch and store AMC, Fund, Portfolio, and Holdings data from Morningstar API'
    ACCESS_TOKEN= "Sv4UAoUpoQ7JGqx2btOQHQhbdmhk"

    def handle(self, *args, **kwargs):
        try:
            ids_df = pd.read_csv(r'C:\Users\nites\Desktop\MF\data.csv').dropna()  # Adjust path
            ids_list = ids_df['ID'].tolist()
            scheme_lit=ids_df['scheme_code'].tolist()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read CSV file: {str(e)}"))
            return

        self.fetch_fund_data(ids_list)
        self.fetch_portfolio_data(ids_list)
        self.fetch_and_save_risk_volatility(ids_list)

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
            url=f"https://api-global.morningstar.com/sal-service/v1/fund/quote/v4/{fund_id}/data?fundServCode=&showAnalystRatingChinaFund=false&showAnalystRating=false&languageId=en&locale=en&clientId=RSIN_SAL&benchmarkId=mstarorcat&component=sal-mip-quote&version=4.13.0&access_token={self.ACCESS_TOKEN}"
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

    def fetch_portfolio_data(self, ids):
        for fund_id in ids:
            url = f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/holding/v2/{id}/data?premiumNum=100&freeNum=25&hideesg=true&languageId=en&locale=en&clientId=RSIN_SAL&benchmarkId=mstarorcat&component=sal-mip-holdings&version=4.31.0&access_token={self.ACCESS_TOKEN}"
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
                        'portfolio_date': pd.to_datetime(portfolio_data.get("portfolioDate"), errors='coerce').date() if portfolio_data.get("portfolioDate") else None,
                        'top_holding_weighting': portfolio_data.get("topHoldingWeighting", 0.0),
                        'last_turnover': portfolio_data.get("lastTurnover", None),
                        'last_turnover_date': pd.to_datetime(portfolio_data.get("LastTurnoverDate"), errors='coerce').date() if portfolio_data.get("LastTurnoverDate") else None,
                        'average_turnover_ratio': portfolio_data.get("averageTurnoverRatio", None),
                        'women_directors_percentage': portfolio_data.get("womenDirectors", 0.0),
                        'women_executives_percentage': portfolio_data.get("womenExecutives", 0.0),
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

    def fetch_amc(self,ids):
        for fund_id in ids:
            url=f""
            response= self.fetch_data(url)
            if not response:
                continue
            data=response.json()

    def fetch_and_save_risk_volatility(self, ids):
        for fund_id in ids:
            url = f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskVolatility/{fund_id}/data?currency=&longestTenure=false&languageId=en&locale=en&clientId=RSIN_SAL&benchmarkId=mstarorcat&component=sal-mip-risk-volatility-measures&version=4.13.0&access_token={self.ACCESS_TOKEN}"
            response = self.fetch_data(url)
            if not response:
                continue
            data = response.json()
            fund_risk_volatility = data.get("fundRiskVolatility", {})
            category_risk_volatility = data.get("categoryRiskVolatility", {})
            timeframes = ["for1Year", "for3Year", "for5Year"]

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

                # Create or update RiskVolatility entry
                RiskVolatility.objects.update_or_create(
                    fund_id=fund_id,
                    defaults={
                        **defaults,
                        'index_name': data.get('indexName'),
                        'fund_name': data.get('fundName'),
                        'category_name': data.get('categoryName'),
                        'calculation_benchmark': data.get('calculationBenchmark'),
                    }
                )