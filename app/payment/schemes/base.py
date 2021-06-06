import json

from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse

from wallet.helpers import ftoi, itos, ftos
from exchange import exchange
from json_logging import log

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

    def set_transaction(self, transaction_id):
        self.transaction = Transaction.objects.get(id=transaction_id)

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
        self.transaction_id = t.id
        self.to_currency = self.system.payment_currency.iso
        self.from_currency = self.wallet.currency.iso
        if self.from_currency != self.to_currency:
            self.converted_amount = exchange.conv(float(self.str_amount), self.from_currency, self.to_currency)
            self.converted_amount_str = ftos(self.converted_amount, self.wallet.currency.digest)

    def success_payment(self, request):
        return render(request, 'payment/success_payment.html')

    def process_payment(self, request, params: dict = None):
        if self.transaction is None:
            if self.transaction_id is not None:
                self.transaction = Transaction.objects.get(id=self.transaction_id)
            else:
                return HttpResponse('')
        self.transaction.status_id = PaymentStatus.DONE
        self.transaction.save()
        return HttpResponse(params.get('response', ''))
