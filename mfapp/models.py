from django.db import models

from django.db import models

class CSVData(models.Model):

    isin= models.CharField(max_length=100,primary_key=True)
    scheme_code = models.CharField(max_length=50)
    ID = models.CharField(max_length=50)
    schem_name = models.CharField(max_length=100)


class Fund(models.Model):
    sec_id = models.CharField(max_length=255, null=True, blank=True)
    isin = models.CharField(max_length=255, null=True, blank=True,unique=True)
    investment_name = models.CharField(max_length=255, null=True, blank=True)
    inceptionDate = models.DateField(null=True, blank=True)
    prospectus_benchmark_name = models.CharField(max_length=255, null=True, blank=True)
    expense_ratio = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    last_turnover_ratio = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    equity_style_box = models.CharField(max_length=255, null=True, blank=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    morningstar_rating = models.IntegerField(null=True, blank=True)
    total_asset = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

class Dt(models.Model):
    scheme_id = models.CharField(max_length=25, blank=True, null=True)
    one_month_return = models.FloatField(null=True, blank=True)
    six_month_return = models.FloatField(null=True, blank=True)
    one_year_return = models.FloatField(null=True, blank=True)
    three_year_return = models.FloatField(null=True, blank=True)
    five_year_return = models.FloatField(null=True, blank=True)


class RiskVolatility(models.Model):
    fund_id = models.CharField(max_length=100, primary_key=True)
    fund_name = models.CharField(max_length=255, null=True, blank=True)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    index_name = models.CharField(max_length=255, null=True, blank=True)
    calculation_benchmark = models.CharField(max_length=255, null=True, blank=True)

    # Fund Risk Volatility for different time periods
    fund_alpha_1y = models.FloatField(null=True, blank=True)
    fund_beta_1y = models.FloatField(null=True, blank=True)
    fund_r_squared_1y = models.FloatField(null=True, blank=True)
    fund_std_dev_1y = models.FloatField(null=True, blank=True)
    fund_sharpe_1y = models.FloatField(null=True, blank=True)

    fund_alpha_3y = models.FloatField(null=True, blank=True)
    fund_beta_3y = models.FloatField(null=True, blank=True)
    fund_r_squared_3y = models.FloatField(null=True, blank=True)
    fund_std_dev_3y = models.FloatField(null=True, blank=True)
    fund_sharpe_3y = models.FloatField(null=True, blank=True)

    fund_alpha_5y = models.FloatField(null=True, blank=True)
    fund_beta_5y = models.FloatField(null=True, blank=True)
    fund_r_squared_5y = models.FloatField(null=True, blank=True)
    fund_std_dev_5y = models.FloatField(null=True, blank=True)
    fund_sharpe_5y = models.FloatField(null=True, blank=True)


    # Category Risk Volatility
    category_alpha_1y = models.FloatField(null=True, blank=True)
    category_beta_1y = models.FloatField(null=True, blank=True)
    category_r_squared_1y = models.FloatField(null=True, blank=True)
    category_std_dev_1y = models.FloatField(null=True, blank=True)
    category_sharpe_1y = models.FloatField(null=True, blank=True)

    category_alpha_3y = models.FloatField(null=True, blank=True)
    category_beta_3y = models.FloatField(null=True, blank=True)
    category_r_squared_3y = models.FloatField(null=True, blank=True)
    category_std_dev_3y = models.FloatField(null=True, blank=True)
    category_sharpe_3y = models.FloatField(null=True, blank=True)

    category_alpha_5y = models.FloatField(null=True, blank=True)
    category_beta_5y = models.FloatField(null=True, blank=True)
    category_r_squared_5y = models.FloatField(null=True, blank=True)
    category_std_dev_5y = models.FloatField(null=True, blank=True)
    category_sharpe_5y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.fund_name} - {self.fund_id}"

class Portfolio(models.Model):
    master_portfolio_id = models.CharField(max_length=255,unique=True)
    sec_id = models.CharField(max_length=255,null=True, blank=True)
    base_currency_id = models.CharField(max_length=10,null=True, blank=True)
    domicile_country_id = models.CharField(max_length=10,null=True, blank=True)
    number_of_holding = models.IntegerField(null=True, blank=True)
    number_of_equity_holding = models.IntegerField(null=True, blank=True)
    portfolio_date = models.DateField(null=True, blank=True)
    top_holding_weighting = models.FloatField(null=True, blank=True)
    last_turnover = models.FloatField(null=True, blank=True)
    last_turnover_date = models.DateField(null=True, blank=True)
    average_turnover_ratio = models.FloatField(null=True, blank=True)
    women_directors_percentage = models.FloatField(null=True, blank=True)
    women_executives_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Portfolio {self.master_portfolio_id} - {self.sec_id}"


class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='holdings', on_delete=models.CASCADE)
    security_name = models.CharField(max_length=255,null=True, blank=True)
    sec_id = models.CharField(max_length=255,null=True, blank=True)
    weighting = models.FloatField(null=True, blank=True)
    number_of_share = models.IntegerField(null=True, blank=True)
    market_value = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    ticker = models.CharField(max_length=10,null=True, blank=True)
    sector = models.CharField(max_length=100,null=True, blank=True)
    total_return_1_year = models.FloatField(null=True, blank=True)
    forward_pe_ratio = models.FloatField(null=True, blank=True)
    stock_rating = models.IntegerField(null=True, blank=True)
    assessment = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return f"Holding {self.security_name} ({self.ticker})"
