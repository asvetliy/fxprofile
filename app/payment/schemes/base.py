import json

from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse

from exchange import exchange
from json_logging import log
from mailer import Mailer
from math_helper import ftoi, itos, ftos, itof

from ..models import PaymentSystem
from ..constants import PaymentStatus

Wallet = apps.get_model('wallet', 'Wallet')
Transaction = apps.get_model('wallet', 'Transaction')
TransactionType = apps.get_model('wallet', 'TransactionType')


class BaseScheme(object):
    def __init__(self, payment_system: PaymentSystem):
        self.amount: float = 0
        self.str_amount: str = ''
        self.int_amount: int = 0
        self.fee_amount: int = 0
        self.converted_amount: float = 0
        self.converted_amount_str: str = ''
        self.transaction_id: int = 0
        self.system: PaymentSystem = payment_system
        self.wallet: Wallet = None
        self.from_currency: str = ''
        self.to_currency: str = ''
        self.transaction: Transaction = None

    def set_wallet(self, wallet_id):
        self.wallet = Wallet.objects.get(id=wallet_id)

    def set_transaction_by_id(self, transaction_id):
        try:
            self.transaction = Transaction.objects.get(id=transaction_id)
            self.transaction_id = transaction_id
        except Transaction.DoesNotExist:
            self.transaction = None
            self.transaction_id = 0

    def set_transaction(self, transaction: Transaction):
        self.transaction = transaction
        self.transaction_id = transaction.id

    def get_amount_with_fee(self, amount: int) -> int:
        if self.system.fee > 0:
            amount += int((self.system.fee / 100) * amount)
        return amount

    @staticmethod
    def get_json_post_data(request):
        try:
            return json.dumps(request.POST, indent=2)
        except Exception as e:
            log.exception(e, exc_info=False)

    def init_system_by_id(self, payment_system_id):
        self.system = PaymentSystem.objects.get(code=payment_system_id)

    def init_payment(self, request):
        if self.transaction is None:
            self.amount = float(request.POST.get('amount', 0))
            self.int_amount = ftoi(self.amount, self.wallet.currency.digest)
            self.fee_amount = self.get_amount_with_fee(self.int_amount)
            self.str_amount = itos(self.fee_amount, self.wallet.currency.digest)
            transaction_type = TransactionType.objects.get(name='deposit')
            t = Transaction.objects.create(
                wallet=self.wallet,
                amount=self.int_amount,
                user=request.user,
                from_to_wallet=self.system.name,
                type=transaction_type,
                status_id=PaymentStatus.PROCESS,
                description=f'Deposit via {self.system.name}'
            )
            self.transaction = t
            self.transaction_id = t.id
        else:
            self.wallet = self.transaction.wallet
            self.amount = itof(self.transaction.amount, self.wallet.currency.digest)
            self.int_amount = self.transaction.amount
            self.fee_amount = self.get_amount_with_fee(self.int_amount)
            self.str_amount = itos(self.fee_amount, self.wallet.currency.digest)
        if self.system.payment_currency:
            self.to_currency = self.system.payment_currency.iso
        else:
            self.to_currency = self.wallet.currency.iso
        self.from_currency = self.wallet.currency.iso
        if self.from_currency != self.to_currency:
            self.converted_amount = exchange.conv(
                float(self.str_amount),
                self.from_currency,
                self.to_currency,
                self.system.exchange_rounding
            )
            self.converted_amount_str = ftos(self.converted_amount, self.system.payment_currency.digest)
        else:
            self.converted_amount = itof(self.fee_amount, self.wallet.currency.digest)
            self.converted_amount_str = self.str_amount
        Mailer.send_managers('init_payment', f'{self.system.code} payment initiated', {
            'payment_system': self,
            'user': request.user,
        })

    def success_payment(self, request):
        return render(request, 'payment/success_payment.html')

    def fail_payment(self, request):
        return render(request, 'payment/fail_payment.html')

    def process_payment(self, request, params: dict = None):
        return HttpResponse('')
