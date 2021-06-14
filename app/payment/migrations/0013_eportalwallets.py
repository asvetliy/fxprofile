# Generated by Django 3.1.5 on 2021-06-14 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0012_auto_20210614_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='EportalWallets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ewallet', models.CharField(max_length=42)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'payment_eportal_wallets',
            },
        ),
    ]