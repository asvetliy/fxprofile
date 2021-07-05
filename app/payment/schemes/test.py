from django.shortcuts import render

from .base import BaseScheme


class TestPayment(BaseScheme):
    def init_payment(self, request, context=None):
        super(TestPayment, self).init_payment(request)
        return render(request, f'payment/{self.system.code}.html', context=context)

    def process_payment(self, request, params=None):
        self.amount = request.POST['amount']
        self.transaction_id = request.POST['transaction_id']
        params = {}
        return super(TestPayment, self).process_payment(request, params=params)
