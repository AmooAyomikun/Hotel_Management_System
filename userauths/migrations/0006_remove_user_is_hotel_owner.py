# Generated by Django 4.2.6 on 2024-09-09 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_user_is_hotel_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_hotel_owner',
        ),
    ]
