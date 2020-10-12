# Generated by Django 2.2 on 2019-09-01 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('LOGIN', models.IntegerField(db_column='LOGIN', primary_key=True, serialize=False, verbose_name='LOGIN')),
                ('GROUP', models.CharField(db_column='GROUP', max_length=16, verbose_name='GROUP')),
            ],
            options={
                'db_table': 'MT4_USERS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trades',
            fields=[
                ('LOGIN', models.IntegerField(db_column='LOGIN', primary_key=True, serialize=False, verbose_name='LOGIN')),
                ('SYMBOL', models.CharField(db_column='SYMBOL', max_length=16, verbose_name='SYMBOL')),
                ('PROFIT', models.FloatField(db_column='PROFIT', verbose_name='PROFIT')),
                ('VOLUME', models.PositiveIntegerField(db_column='VOLUME', verbose_name='VOLUME')),
            ],
            options={
                'db_table': 'MT4_TRADES',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'account_types',
            },
        ),
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pamm', models.BooleanField()),
                ('pwd', models.CharField(max_length=32)),
                ('inv_pwd', models.CharField(max_length=32)),
                ('phone_pwd', models.CharField(max_length=32)),
                ('account_id', models.IntegerField(db_column='account_id', verbose_name='account_id')),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mt4.AccountTypes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
    ]
