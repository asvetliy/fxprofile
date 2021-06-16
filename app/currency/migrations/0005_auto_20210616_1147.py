from django.db import migrations


def create_currencies(apps, schema_editor):
    Currency = apps.get_model('currency', 'Currency')
    Currency.objects.create(
        iso='BTC', symbol='BTC', name='Bitcoin',
        digest=8, is_default=False, is_base=False, is_enabled=False
    )


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0004_auto_20210606_2205'),
    ]

    operations = [
        migrations.RunPython(create_currencies),
    ]
