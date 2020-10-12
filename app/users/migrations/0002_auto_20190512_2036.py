from django.db import models, migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name='Administrators'),
        Group(name='Registered'),
    ])


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            'Administrators',
            'Registered',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]