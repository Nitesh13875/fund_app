# Generated by Django 5.1.2 on 2024-10-29 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mfapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='women_directors_percentage',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='women_executives_percentage',
        ),
        migrations.RemoveField(
            model_name='riskvolatility',
            name='calculation_benchmark',
        ),
    ]
