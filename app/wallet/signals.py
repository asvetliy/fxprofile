from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import Wallet, Transaction

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_wallets(sender, instance, created, **kwargs):
    if created:
        Currency = apps.get_model('currency', 'Currency')
        currencies = Currency.objects.filter(is_enabled=True)
        for currency in currencies:
            Wallet.objects.create(user=instance, currency=currency)


@receiver(post_save, sender=Transaction)
def balance_changed(sender, instance, created, **kwargs):
    wallet = instance.get_wallet()
    balance = Transaction.objects.filter(wallet=wallet, status_id=1).aggregate(Sum('amount'))
    if balance['amount__sum'] is not None:
        wallet.balance = balance['amount__sum']
        wallet.save()
