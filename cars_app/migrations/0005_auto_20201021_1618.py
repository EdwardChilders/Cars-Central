# Generated by Django 2.2.4 on 2020-10-21 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0004_auto_20201021_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]