# Generated by Django 3.0.7 on 2020-06-26 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0008_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tngproducts',
            name='Additional_Details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
