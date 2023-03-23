# Generated by Django 4.1.7 on 2023-03-11 17:04

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardNumber', models.CharField(max_length=16, validators=[accounts.models.validateCardNumber])),
                ('expirationDate', models.CharField(max_length=5, validators=[accounts.models.validateExpirationDate])),
                ('cvv', models.CharField(max_length=4, validators=[accounts.models.validate_cvv])),
                ('cardHolderName', models.CharField(max_length=255, validators=[accounts.models.validate_cardholder_name])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('userType', models.CharField(choices=[('C', 'Customer'), ('S', 'Student'), ('CR', 'Club Rep'), ('AM', 'Accounts Manager'), ('CM', 'Cinema Manager'), ('SU', 'Super User')], default='C', max_length=2)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('dateOfBirth', models.DateField()),
                ('paymentDetails', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.paymentdetails')),
            ],
        ),
    ]