# Generated by Django 3.1.5 on 2021-06-04 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_paymentsystem_payment_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentsystem',
            name='config',
            field=models.JSONField(db_column='config', default=dict, verbose_name='config'),
        ),
    ]