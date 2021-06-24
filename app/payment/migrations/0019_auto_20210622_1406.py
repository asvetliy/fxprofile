from django.db import migrations


def create_rockspay_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    Currency = apps.get_model('currency', 'Currency')
    PaymentSystem.objects.create(
        name='RocksPay',
        is_enabled=True,
        code='rockspay',
        config={
            "callback_url": "https://xyz.trading/payments/rockspay/process",
            "merchant_id": "39e6ecd5-f11b-4bbb-a1e7-ac085b611c87",
            "secret_key": "NBHcPVDJxidxitCaItakuf1VF6Wwj7IA",
            "duration": 3600,
            "additional_fields": [
                {
                    "name": "card_number",
                    "type": "card_number",
                }
            ],
        },
        payment_currency=Currency.objects.get(iso='RUB'),
        fee=5,
        position=6,
        min_amount=15,
        max_amount=600,
        cls='RockspayPayment'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_auto_20210622_1402'),
    ]

    operations = [
        migrations.RunPython(create_rockspay_payment),
    ]
