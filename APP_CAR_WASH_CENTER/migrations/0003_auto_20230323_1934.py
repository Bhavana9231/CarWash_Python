# Generated by Django 3.1 on 2023-03-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_CAR_WASH_CENTER', '0002_auto_20230323_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timings',
            name='Stime',
            field=models.TimeField(default=None, max_length=100, null=True),
        ),
    ]
