# Generated by Django 3.0.7 on 2020-08-18 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0020_auto_20200818_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tngproducts',
            name='label',
            field=models.CharField(choices=[('P', 'BESTSELLER'), ('D', 'NEW'), ('H', 'HotDeals'), ('R', 'Regular')], default='R', max_length=1),
        ),
    ]