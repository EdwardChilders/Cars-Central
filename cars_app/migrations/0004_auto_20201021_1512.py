# Generated by Django 2.2.4 on 2020-10-21 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0003_car_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='img',
            field=models.ImageField(upload_to='images/'),
        ),
    ]