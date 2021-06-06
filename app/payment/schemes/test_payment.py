from django.shortcuts import render

from .base import BaseScheme


class TestPayment(BaseScheme):
    def init_payment(self, request, context=None):
        context = {
            'amount': self.amount,
            'transaction_id': self.transaction_id
        }
        return super(TestPayment, self).init_payment(request, context)

    def process_payment(self, request, params=None):
        self.amount = request.POST['amount']
        self.transaction_id = request.POST['transaction_id']
        self.status = request.POST['status']

        params = {}
        return super(TestPayment, self).process_payment(request, params=params)
