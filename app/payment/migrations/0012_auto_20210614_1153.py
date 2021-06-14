from django.db import migrations


def create_eportal_payment(apps, schema_editor):
    PaymentSystem = apps.get_model('payment', 'PaymentSystem')
    PaymentSystem.objects.create(
        name='Portal (Global)',
        is_enabled=True,
        code='eportal',
        config={
            "secret_key": "iW1wA4bZ6eZ1yF6r",
            "merchant_id": "GR02",
        },
        payment_currency=None,
        fee=4,
        position=4,
        cls='EportalPayment',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_auto_20210607_1823'),
    ]

    operations = [
        migrations.RunPython(create_eportal_payment),
    ]
