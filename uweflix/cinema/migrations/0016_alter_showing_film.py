# Generated by Django 4.1.5 on 2023-03-22 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0015_alter_film_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='film',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.film'),
        ),
    ]