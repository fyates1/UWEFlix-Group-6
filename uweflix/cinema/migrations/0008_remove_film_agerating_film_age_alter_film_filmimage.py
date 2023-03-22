# Generated by Django 4.1.5 on 2023-03-21 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_alter_showing_date_alter_showing_numberofsales_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='ageRating',
        ),
        migrations.AddField(
            model_name='film',
            name='age',
            field=models.IntegerField(choices=[(0, 'U'), (1, 'PG'), (2, '12A'), (3, '12'), (4, '15'), (5, '18')], default=5),
        ),
        migrations.AlterField(
            model_name='film',
            name='filmImage',
            field=models.ImageField(upload_to='cinema/static/images/'),
        ),
    ]
