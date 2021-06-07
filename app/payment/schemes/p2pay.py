import json

from django.shortcuts import render
from django.http import HttpResponse

from mailer import Mailer

from .base import BaseScheme


class P2PayPayment(BaseScheme):
    NAME = 'P2Pay'

    def init_payment(self, request):
        super(P2PayPayment, self).init_payment(request)
        received_data = json.dumps({
            'user': {
                'username': request.user.username,
                'email': request.user.email,
                'id': request.user.id,
            },
            'transaction_id': self.transaction_id,
            'currency': self.to_currency,
            'amount': self.converted_amount_str,
            'order_currency': self.from_currency,
            'order_amount': self.str_amount,
        })
        Mailer.send_managers('successful_payment', f'Received initial payment from - {self.NAME}', {
            'received_data': received_data,
            'payment_system': {self.NAME},
        })
        return render(request, f'payment/{self.system.code}.html', context={})

    def process_payment(self, request, params=None):
        return HttpResponse('')
