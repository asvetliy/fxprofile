from django.db import migrations


def create_p2pay_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    Currency = apps.get_model('currency', 'Currency')
    PaymentSystem.objects.create(
        name='P2Pay',
        is_enabled=True,
        code='p2pay',
        config=dict,
        payment_currency=Currency.objects.get(iso='RUB'),
        fee=5,
        position=3,
        cls='P2PayPayment'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20210607_1437'),
    ]

    operations = [
        migrations.RunPython(create_p2pay_payment),
    ]
