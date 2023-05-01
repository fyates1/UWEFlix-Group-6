# Generated by Django 4.1.4 on 2023-05-01 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0024_alter_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='adult_tickets',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='booking',
            name='child_tickets',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='booking',
            name='cr_tickets',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='student_tickets',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='screen',
            name='capacity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='seat',
            name='number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='showing',
            name='numberOfSales',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]