# Generated by Django 3.0.7 on 2020-08-11 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0016_auto_20200811_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='tngproducts',
            options={'verbose_name_plural': 'Products'},
        ),
    ]
