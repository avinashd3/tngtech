# Generated by Django 3.0.7 on 2020-08-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0026_auto_20200826_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tngproducts',
            name='slug',
            field=models.SlugField(default='random.choices(string.ascii_lowercase + string.digits, k=6)'),
        ),
    ]