# Generated by Django 2.2 on 2019-05-19 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0009_auto_20190519_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
