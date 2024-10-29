from django.contrib import admin
from .models import Fund, AMC ,Portfolio, Holding, RiskVolatility

# # # Register your models
admin.site.register(Fund)
# admin.site.register(AMC)
# admin.site.register(Dt)
admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(RiskVolatility)