# Generated by Django 3.0.7 on 2020-08-19 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0003_auto_20200819_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='shophome',
            name='linkname',
            field=models.CharField(default='Shop Now', max_length=20),
        ),
    ]
