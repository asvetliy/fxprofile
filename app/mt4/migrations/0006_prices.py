# Generated by Django 3.1.5 on 2021-05-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mt4', '0005_auto_20200413_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('SYMBOL', models.CharField(db_column='SYMBOL', max_length=16, primary_key=True, serialize=False, verbose_name='SYMBOL')),
                ('TIME', models.DateTimeField(db_column='TIME', verbose_name='TIME')),
                ('BID', models.FloatField(db_column='BID', verbose_name='BID')),
                ('ASK', models.FloatField(db_column='ASK', verbose_name='ASK')),
                ('LOW', models.FloatField(db_column='LOW', verbose_name='LOW')),
                ('HIGH', models.FloatField(db_column='HIGH', verbose_name='HIGH')),
                ('DIRECTION', models.IntegerField(db_column='DIRECTION', verbose_name='DIRECTION')),
                ('DIGITS', models.IntegerField(db_column='DIGITS', verbose_name='DIGITS')),
                ('SPREAD', models.IntegerField(db_column='SPREAD', verbose_name='SPREAD')),
                ('MODIFY_TIME', models.DateTimeField(db_column='MODIFY_TIME', verbose_name='MODIFY_TIME')),
            ],
            options={
                'verbose_name_plural': 'mt4 prices',
                'db_table': 'MT4_PRICES',
                'managed': False,
            },
        ),
    ]
