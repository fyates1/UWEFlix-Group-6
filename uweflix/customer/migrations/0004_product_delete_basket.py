# Generated by Django 4.1.4 on 2023-03-30 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_basket_remove_ticketbooking_credit_card_exp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
