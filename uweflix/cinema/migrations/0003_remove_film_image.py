# Generated by Django 4.1.7 on 2023-03-18 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_film_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='image',
        ),
    ]
