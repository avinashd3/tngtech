# Generated by Django 3.0.7 on 2020-09-26 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0040_auto_20200926_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tngproducts',
            name='color',
        ),
        migrations.AddField(
            model_name='tngproducts',
            name='color',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prod.Colors'),
        ),
    ]
