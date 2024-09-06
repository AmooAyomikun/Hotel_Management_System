# Generated by Django 5.0.6 on 2024-08-30 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('Booking Confirmed', 'Booking Confirmed'), ('Booking Cancelled', 'Booking Cancelled')], default='new_order', max_length=100),
        ),
    ]
