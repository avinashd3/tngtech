# Generated by Django 3.0.7 on 2020-08-11 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0015_auto_20200811_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tngproducts',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='tngproducts',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='tngproducts',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='tngproducts',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
    ]
