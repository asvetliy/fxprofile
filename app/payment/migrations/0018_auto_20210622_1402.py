# Generated by Django 3.1.5 on 2021-06-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_auto_20210616_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentsystem',
            name='max_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paymentsystem',
            name='min_amount',
            field=models.IntegerField(default=0),
        ),
    ]