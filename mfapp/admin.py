from django.contrib import admin
from .models import Fund ,Portfolio, Holding, RiskVolatility,Dt,CSVData,Settings,StockDataRefresh
#
# # # Register your models
admin.site.register(Fund)
admin.site.register(Dt)
admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(RiskVolatility)
admin.site.register(CSVData)
admin.site.register(Settings)
admin.site.register(StockDataRefresh)
