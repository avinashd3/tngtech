# Generated by Django 3.0.7 on 2020-08-21 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0008_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotdeals',
            name='days',
        ),
        migrations.RemoveField(
            model_name='hotdeals',
            name='hours',
        ),
        migrations.RemoveField(
            model_name='hotdeals',
            name='minutes',
        ),
        migrations.RemoveField(
            model_name='hotdeals',
            name='seconds',
        ),
    ]
