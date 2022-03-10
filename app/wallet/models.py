from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from math_helper import int_to_amount, itof


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
    from_to_wallet = models.CharField(max_length=64, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)
    description = models.CharField(max_length=128, default=None, blank=True)

    def __init__(self, *args, **kwargs):
        self.changed_data = {}
        super(Transaction, self).__init__(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def get_wallet(self):
        return self.wallet

    def _get_transaction_amount(self):
        return int_to_amount(self.amount, self.wallet.currency.digest)

    transaction_amount = property(_get_transaction_amount)

    def save(self, *args, **kwargs):
        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            update_fields = {}
            for field in cls._meta.get_fields():
                try:
                    if getattr(old, field.name) != getattr(new, field.name):
                        update_fields[field.name] = getattr(old, field.name)
                except Exception as e:  # Catch field does not exist exception
                    pass
            self.changed_data = update_fields
        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        db_table = 'transactions'
