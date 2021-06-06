from django.db import migrations


def create_paythrone_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    Currency = apps.get_model('currency', 'Currency')
    PaymentSystem.objects.create(
        name='VISA / MasterCard / MIR',
        is_enabled=True,
        code='paythrone',
        config={
            "public_key": "",
            "private_key": "",
        },
        payment_currency=Currency.objects.get(iso='RUB'),
        fee=3,
        cls='PaythronePayment'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20210604_0044'),
    ]

    operations = [
        migrations.RunPython(create_paythrone_payment),
    ]
