from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse
from ..models import PaymentSystem

Wallet = apps.get_model('wallet', 'Wallet')
Transaction = apps.get_model('wallet', 'Transaction')
TransactionType = apps.get_model('wallet', 'TransactionType')
TransactionStatus = apps.get_model('wallet', 'TransactionStatus')


class BaseScheme(object):
    amount = 0
    transaction_id = 0

    @staticmethod
    def amount_to_balance(amount):
        return int(float(amount) * 100)

    def init_payment(self, request):
        account_id = request.POST['account']
        payment_system_id = request.POST['payment_system']
        amount = self.amount_to_balance(request.POST['amount'])

        payment_system = PaymentSystem.objects.get(code=payment_system_id)
        transaction_type = TransactionType.objects.get(name='deposit')
        transaction_status = TransactionStatus.objects.get(name='process')

        w = Wallet.objects.get(id=account_id)
        t = Transaction.objects.create(
            wallet=w,
            amount=amount,
            user=request.user,
            from_to_wallet=payment_system.code,
            type=transaction_type,
            status=transaction_status,
            description=f'Deposit via {payment_system.name}'
        )
        self.transaction_id = t.id
        self.amount = amount

    def success_payment(self, request):
        return render(request, 'payment/success_payment.html')

    def process_payment(self, request, params=None):
        if params is not None:
            transaction = Transaction.objects.get(id=params['transaction_id'])
            transaction_status = TransactionStatus.objects.get(name='done')
            transaction.status = transaction_status
            transaction.save()
        return HttpResponse('')
