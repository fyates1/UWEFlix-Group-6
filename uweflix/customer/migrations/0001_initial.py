# Generated by Django 4.1.4 on 2023-03-24 10:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinema', '0016_alter_showing_film'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_date', models.DateField(default=django.utils.timezone.now)),
                ('ticket_count', models.IntegerField()),
                ('ticket_type', models.CharField(choices=[(1, 'Student'), (2, 'Child'), (3, 'Adult')], max_length=15)),
                ('credit_card_info', models.CharField(max_length=30)),
                ('credit_card_name', models.CharField(max_length=30)),
                ('credit_card_exp', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.showing')),
            ],
        ),
    ]
