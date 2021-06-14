from django.db import models
from django.conf import settings


class PaymentSystem(models.Model):
    name = models.CharField(max_length=64, default=None)
    code = models.CharField(max_length=32, blank=False)
    cls = models.CharField(max_length=32, blank=False)
    is_enabled = models.BooleanField(blank=False, default=False)
    withdraw = models.BooleanField(blank=False, default=False)
    fee = models.IntegerField(blank=False, default=0)
    position = models.IntegerField(blank=False, default=0)
    payment_currency = models.ForeignKey(settings.CURRENCY_MODEL, models.CASCADE, blank=False, null=True)
    config = models.JSONField(
        db_column='config',
        verbose_name='config',
        name='config',
        blank=True,
        null=True,
        default=dict
    )

    class Meta:
        db_table = 'payment_systems'


class EportalWallets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, null=True, blank=False)
    ewallet = models.CharField(max_length=42, blank=False, null=False)

    class Meta:
        db_table = 'payment_eportal_wallets'
