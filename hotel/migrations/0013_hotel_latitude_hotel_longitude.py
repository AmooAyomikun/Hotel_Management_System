# Generated by Django 4.2.6 on 2024-09-09 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0012_alter_hotel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
