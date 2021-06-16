from django.db import migrations


def create_blockchain_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    Currency = apps.get_model('currency', 'Currency')
    PaymentSystem.objects.create(
        name='Blockchain',
        is_enabled=True,
        code='blockchain',
        config={
            "expire_time": 15*60,
        },
        payment_currency=Currency.objects.get(iso='BTC'),
        fee=3,
        position=5,
        cls='BlockchainPayment'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_blockchainwallet'),
    ]

    operations = [
        migrations.RunPython(create_blockchain_payment),
    ]
