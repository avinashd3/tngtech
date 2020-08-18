# Generated by Django 3.0.7 on 2020-08-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0017_auto_20200811_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='tngproducts',
            name='brand',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='tngproducts',
            name='subcategory',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='tngproducts',
            name='category',
            field=models.CharField(choices=[('MA', 'Mobile Accessories'), ('LA', 'Laptop Accessories'), ('TA', 'Tablet Accessories'), ('EG', 'Electronic Gadgets'), ('LA', 'Latest Accessories'), ('MR', 'Mobile Repair'), ('LR', 'Laptop/Computer Repair'), ('TR', 'iPad/Tablet Repair')], default='A', max_length=2),
        ),
    ]
