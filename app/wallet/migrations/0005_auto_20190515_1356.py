# Generated by Django 2.2 on 2019-05-15 13:56

from django.db import migrations


def create_transaction_types(apps, schema_editor):
    TransactionType = apps.get_model('wallet', 'TransactionType')
    TransactionType.objects.create(
        name='deposit'
    )
    TransactionType.objects.create(
        name='withdraw'
    )
    TransactionType.objects.create(
        name='bonus'
    )
    TransactionType.objects.create(
        name='transfer_in'
    )
    TransactionType.objects.create(
        name='transfer_out'
    )
    TransactionType.objects.create(
        name='fee'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_auto_20190515_1303'),
    ]

    operations = [
        migrations.RunPython(create_transaction_types),
    ]
