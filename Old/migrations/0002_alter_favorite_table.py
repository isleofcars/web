# Generated by Django 3.2.7 on 2022-12-06 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='favorite',
            table='ads_favorite',
        ),
    ]