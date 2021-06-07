from django.db import migrations


def create_freekassa_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    Currency = apps.get_model('currency', 'Currency')
    PaymentSystem.objects.create(
        name='FREEKASSA',
        is_enabled=True,
        code='freekassa',
        config={
            "merchant_id": "547",
            "secret_key": "",
            "secret_key2": "",
        },
        payment_currency=Currency.objects.get(iso='RUB'),
        fee=8,
        position=2,
        cls='FreekassaPayment'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_paymentsystem_position'),
    ]

    operations = [
        migrations.RunPython(create_freekassa_payment),
    ]
