# Generated by Django 3.0.7 on 2020-09-29 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0044_auto_20200929_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colors',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prod.TngProducts'),
        ),
    ]
