# Generated by Django 3.0.7 on 2020-08-10 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0013_onlinebooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='tngproducts',
            name='image1',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='tngproducts',
            name='image2',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='tngproducts',
            name='image3',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='tngproducts',
            name='image4',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
    ]