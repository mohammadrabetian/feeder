# Generated by Django 2.2.11 on 2020-11-29 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20201128_1856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'verbose_name': 'Feed', 'verbose_name_plural': 'Feeds'},
        ),
    ]
