# Generated by Django 2.2 on 2019-05-19 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_auto_20190519_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='params',
            field=models.TextField(blank=True, db_column='params', default=None, null=True, verbose_name='params'),
        ),
    ]
