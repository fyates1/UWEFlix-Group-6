# Generated by Django 4.1.7 on 2023-03-16 18:15

import clubRep.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clubName', models.CharField(max_length=255)),
                ('memberCount', models.IntegerField(default=1)),
                ('email', models.CharField(max_length=20)),
                ('landlineNo', models.CharField(max_length=255, null=True, validators=[clubRep.models.isLandlineNumber])),
                ('mobileNo', models.CharField(max_length=20, null=True, validators=[clubRep.models.isMobileNumber])),
                ('discount', models.IntegerField(default=2)),
                ('streetNo', models.IntegerField()),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
            ],
        ),
    ]