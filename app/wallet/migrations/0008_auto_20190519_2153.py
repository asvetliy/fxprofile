# Generated by Django 2.2 on 2019-05-19 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_transaction_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
