# Generated by Django 4.1.4 on 2023-05-08 15:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0027_alter_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='purchase_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
