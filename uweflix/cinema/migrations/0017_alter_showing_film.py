# Generated by Django 4.1.4 on 2023-03-27 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0016_alter_showing_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='film',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='cinema.film'),
        ),
    ]
