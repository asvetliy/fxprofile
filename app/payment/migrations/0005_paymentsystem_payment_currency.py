# Generated by Django 3.1.5 on 2021-06-03 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_auto_20200413_1440'),
        ('payment', '0004_paymentsystem_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentsystem',
            name='payment_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='currency.currency'),
        ),
    ]
