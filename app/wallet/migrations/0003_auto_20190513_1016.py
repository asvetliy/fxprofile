# Generated by Django 2.2 on 2019-05-13 10:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.BigIntegerField(db_column='balance', default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='balance'),
        ),
    ]
