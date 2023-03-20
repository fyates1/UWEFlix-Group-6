# Generated by Django 4.1.7 on 2023-03-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userType',
            field=models.CharField(choices=[('C', 'Customer'), ('S', 'Student'), ('CR', 'Club Rep'), ('AM', 'Accounts Manager'), ('CM', 'Cinema Manager')], default='C', max_length=2),
        ),
    ]
