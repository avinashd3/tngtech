# Generated by Django 3.0.7 on 2020-08-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0034_auto_20200827_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tngproducts',
            name='date',
        ),
        migrations.AlterField(
            model_name='tngproducts',
            name='slug',
            field=models.SlugField(),
        ),
    ]
