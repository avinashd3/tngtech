# Generated by Django 3.0.7 on 2020-08-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0019_onlinebooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinebooking',
            name='time',
            field=models.CharField(max_length=20),
        ),
    ]