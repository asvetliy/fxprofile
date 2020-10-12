# Generated by Django 2.2 on 2019-05-12 20:21

from django.db import migrations


def create_default_currencies(apps, schema_editor):
    Currency = apps.get_model('currency', 'Currency')
    Currency.objects.create(
        iso='USD', symbol='$', name='United State Dollar',
        digest=2, is_default=True, is_base=True, is_enabled=True
    )
    Currency.objects.create(
        iso='EUR', symbol='€', name='Euro',
        digest=2, is_default=False, is_base=False, is_enabled=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_currencies),
    ]
