# Generated by Django 3.1.5 on 2021-07-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0021_paymentsystem_exchange_rounding'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchainwallet',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
