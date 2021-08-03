from django.db import models
from django.conf import settings

from math_helper import ftos


class AccountTypes(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'account_types'


class Accounts(models.Model):
    use_in_migrations = False
    LOGIN = models.IntegerField(verbose_name='LOGIN', db_column='LOGIN', primary_key=True)
    LEVERAGE = models.IntegerField(verbose_name='LEVERAGE', db_column='LEVERAGE')
    GROUP = models.CharField(max_length=16, verbose_name='GROUP', db_column='GROUP')
    CURRENCY = models.CharField(max_length=32, verbose_name='CURRENCY', db_column='CURRENCY')
    BALANCE = models.FloatField(verbose_name='BALANCE', db_column='BALANCE')
    EQUITY = models.FloatField(verbose_name='EQUITY', db_column='EQUITY')
    MARGIN = models.FloatField(verbose_name='MARGIN', db_column='MARGIN')
    MARGIN_FREE = models.FloatField(verbose_name='MARGIN_FREE', db_column='MARGIN_FREE')
    MARGIN_LEVEL = models.FloatField(verbose_name='MARGIN_LEVEL', db_column='MARGIN_LEVEL')
    REGDATE = models.DateTimeField(verbose_name='REGDATE', db_column='REGDATE')
    LASTDATE = models.DateTimeField(verbose_name='LASTDATE', db_column='LASTDATE')

    class Meta:
        managed = False
        db_table = 'MT4_USERS'
        verbose_name_plural = 'mt4 accounts'


class Prices(models.Model):
    use_in_migrations = False
    SYMBOL = models.CharField(verbose_name='SYMBOL', db_column='SYMBOL', max_length=16, primary_key=True)
    TIME = models.DateTimeField(verbose_name='TIME', db_column='TIME')
    BID = models.FloatField(verbose_name='BID', db_column='BID')
    ASK = models.FloatField(verbose_name='ASK', db_column='ASK')
    LOW = models.FloatField(verbose_name='LOW', db_column='LOW')
    HIGH = models.FloatField(verbose_name='HIGH', db_column='HIGH')
    DIRECTION = models.IntegerField(verbose_name='DIRECTION', db_column='DIRECTION')
    DIGITS = models.IntegerField(verbose_name='DIGITS', db_column='DIGITS')
    SPREAD = models.IntegerField(verbose_name='SPREAD', db_column='SPREAD')
    MODIFY_TIME = models.DateTimeField(verbose_name='MODIFY_TIME', db_column='MODIFY_TIME')

    class Meta:
        managed = False
        db_table = 'MT4_PRICES'
        verbose_name_plural = 'mt4 prices'


class UserAccounts(models.Model):
    id = models.BigIntegerField(auto_created=False, primary_key=True, serialize=False, verbose_name='id', db_column='id')
    is_pamm = models.BooleanField()
    pwd = models.CharField(max_length=32)
    inv_pwd = models.CharField(max_length=32)
    phone_pwd = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    account_type = models.ForeignKey(AccountTypes, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(settings.CURRENCY_MODEL, on_delete=models.DO_NOTHING)

    def has_amount(self, amount):
        mt4_account = Accounts.objects.get(LOGIN=self.id)
        return mt4_account.BALANCE >= amount

    class Meta:
        db_table = 'accounts'
        verbose_name_plural = 'user accounts'


class Trades(models.Model):
    use_in_migrations = False
    TICKET = models.IntegerField(verbose_name='TICKET', db_column='TICKET', primary_key=True)
    LOGIN = models.IntegerField(verbose_name='LOGIN', db_column='LOGIN')
    CMD = models.IntegerField(verbose_name='CMD', db_column='CMD')
    SYMBOL = models.CharField(verbose_name='SYMBOL', db_column='SYMBOL', max_length=16)
    PROFIT = models.FloatField(verbose_name='PROFIT', db_column='PROFIT')
    VOLUME = models.PositiveIntegerField(verbose_name='VOLUME', db_column='VOLUME')
    OPEN_TIME = models.DateTimeField(verbose_name='OPEN_TIME', db_column='OPEN_TIME')
    CLOSE_TIME = models.DateTimeField(verbose_name='CLOSE_TIME', db_column='CLOSE_TIME')
    SWAPS = models.FloatField(verbose_name='SWAPS', db_column='SWAPS')
    COMMISSION = models.FloatField(verbose_name='COMMISSION', db_column='COMMISSION')
    OPEN_PRICE = models.FloatField(verbose_name='OPEN_PRICE', db_column='OPEN_PRICE')
    CLOSE_PRICE = models.FloatField(verbose_name='CLOSE_PRICE', db_column='CLOSE_PRICE')
    DIGITS = models.IntegerField(verbose_name='DIGITS', db_column='DIGITS')

    def _get_trade_profit(self):
        return ftos(self.PROFIT, 2)

    trade_profit = property(_get_trade_profit)

    def _get_trade_volume(self):
        return ftos(self.VOLUME/100, 2)

    trade_volume = property(_get_trade_volume)

    def _get_trade_swaps(self):
        return ftos(self.SWAPS, 2)

    trade_swaps = property(_get_trade_swaps)

    def _get_trade_commission(self):
        return ftos(self.COMMISSION, 2)

    trade_commission = property(_get_trade_commission)

    def _get_trade_open_price(self):
        return ftos(self.OPEN_PRICE, 2)

    trade_open_price = property(_get_trade_open_price)

    def _get_trade_close_price(self):
        return ftos(self.CLOSE_PRICE, 2)

    trade_close_price = property(_get_trade_close_price)

    class Meta:
        managed = False
        db_table = 'MT4_TRADES'
        verbose_name_plural = 'mt4 trades'
