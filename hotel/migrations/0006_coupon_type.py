# Generated by Django 5.0.6 on 2024-08-25 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_coupon_bookmark_booking_coupons_couponusers_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='type',
            field=models.CharField(default='Percentage', max_length=100),
        ),
    ]
