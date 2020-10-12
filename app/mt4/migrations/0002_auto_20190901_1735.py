# Generated by Django 2.2 on 2019-05-15 13:03

from django.db import migrations


def create_account_types(apps, schema_editor):
    AccountTypes = apps.get_model('mt4', 'AccountTypes')
    AccountTypes.objects.create(
        name='STP'
    )
    AccountTypes.objects.create(
        name='ECN'
    )
    AccountTypes.objects.create(
        name='VIP'
    )


def remove_account_types(apps, schema_editor):
    AccountTypes = apps.get_model('mt4', 'AccountTypes')
    AccountTypes.objects.filter(name='VIP').delete()
    AccountTypes.objects.filter(name='ECN').delete()
    AccountTypes.objects.filter(name='STP').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mt4', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_account_types, remove_account_types),
    ]
