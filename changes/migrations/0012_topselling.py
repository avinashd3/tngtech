# Generated by Django 3.0.7 on 2020-09-01 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0011_auto_20200826_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopSelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='changes.Category')),
            ],
        ),
    ]
