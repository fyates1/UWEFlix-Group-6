# Generated by Django 4.1.4 on 2023-04-13 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0020_film_trailer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='date',
            field=models.DateField(verbose_name='Date of showing (yyyy/mm/dd)'),
        ),
    ]
