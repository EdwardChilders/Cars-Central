# Generated by Django 2.2.4 on 2020-10-21 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0002_auto_20201020_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='img',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]
