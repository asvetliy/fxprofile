# Generated by Django 3.1.5 on 2021-05-24 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210104_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verificated',
            new_name='is_verified',
        ),
    ]
