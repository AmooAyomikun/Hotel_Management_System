# Generated by Django 5.0.6 on 2024-07-20 01:02

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_booking_activitylog_hotelfaqs_hotelfeatures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
    ]
