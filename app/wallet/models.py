import json
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from .helpers import int_to_amount, itof


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    currency = models.ForeignKey(settings.CURRENCY_MODEL, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return f'{self.user.username} ({self.currency.iso})'

    def get_transactions(self):
        return Transaction.objects.filter(wallet=self)

    def get_user(self):
        return self.user

    def get_balance(self):
        return int_to_amount(self.balance, self.currency.digest)

    def _get_wallet_balance(self):
        return int_to_amount(self.balance, self.currency.digest)

    def has_amount(self, amount):
        return itof(self.balance, self.currency.digest) >= amount

    wallet_balance = property(_get_wallet_balance)

    class Meta:
        db_table = 'wallets'


class TransactionStatus(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'transaction_status'


class TransactionType(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'transaction_type'


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    amount = models.BigIntegerField()
    from_to_wallet = models.CharField(max_length=32, default=None, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)
    description = models.CharField(max_length=128, default=None)
    _params = models.TextField(
        db_column='params',
        verbose_name='params',
        name='params',
        blank=True,
        default=None,
        null=True
    )

    def __str__(self):
        return str(self.id)

    def _get_params(self):
        return json.loads(self._params)

    def _set_params(self, value):
        self._params = json.dumps(value)

    config = property(_get_params, _set_params)

    def get_wallet(self):
        return self.wallet

    def _get_transaction_amount(self):
        return int_to_amount(self.amount, self.wallet.currency.digest)

    transaction_amount = property(_get_transaction_amount)

    class Meta:
        db_table = 'transactions'
