from decimal import Decimal

def safe_decimal(value):
    return Decimal(value) if value not in (None, '') else None