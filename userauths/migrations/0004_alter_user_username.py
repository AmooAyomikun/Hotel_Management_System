# Generated by Django 4.2.6 on 2024-09-06 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
