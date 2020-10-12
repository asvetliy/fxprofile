from django.shortcuts import render
from .base import BaseScheme


class TestPayment(BaseScheme):
    def init_payment(self, request):
        super(TestPayment, self).init_payment(request)
        context = {
            'amount': self.amount,
            'transaction_id': self.transaction_id
        }
        return render(request, 'payment/test_payment.html', context=context)

    def process_payment(self, request, params=None):
        amount = request.POST['amount']
        transaction_id = request.POST['transaction_id']
        status = request.POST['status']

        params = {
            'amount': amount,
            'transaction_id': transaction_id,
            'status': status
        }
        return super(TestPayment, self).process_payment(request, params)
