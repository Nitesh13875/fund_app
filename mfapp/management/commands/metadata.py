from django.core.management.base import BaseCommand
import csv
from mfapp.models import CSVData

class Command(BaseCommand):
    help = 'Imports CSV data into the database'

    def handle(self, *args, **options):
        with open(r'C:\Users\nites\Desktop\MF\data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                isin, scheme_name, scheme_code, scheme_id = row
                CSVData.objects.create(isin=isin, scheme_name=scheme_name, scheme_code=scheme_code,scheme_id=scheme_id)