# Generated by Django 4.1.4 on 2023-04-14 13:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0021_alter_showing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cr_tickets',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
