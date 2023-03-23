# Generated by Django 4.1.7 on 2023-03-20 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_remove_showing_datetime_showing_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date of showing (mm/dd/yyyy)'),
        ),
        migrations.AlterField(
            model_name='showing',
            name='startTime',
            field=models.TimeField(default='11/11/1111'),
        ),
    ]