import hashlib

from django.shortcuts import render
from django.http import HttpResponse

from mailer import Mailer

from .base import BaseScheme
from ..constants import PaymentStatus


class FreekassaPayment(BaseScheme):
    NAME = 'Freekassa'

    @staticmethod
    def create_signature(hash_list: list):
        hash_string = ':'.join(hash_list)
        return hashlib.md5(hash_string.encode('utf-8')).hexdigest()

    def init_payment(self, request):
        super(FreekassaPayment, self).init_payment(request)
        hash_list = [
            self.system.config.get('merchant_id', ''),
            self.converted_amount_str,
            self.system.config.get('secret_key', ''),
            self.to_currency,
            str(self.transaction_id),
        ]
        signature = self.create_signature(hash_list)
        context = {
            'signature': signature,
            'amount': self.converted_amount_str,
            'currency': self.to_currency,
            'transaction_id': self.transaction_id,
            'username': request.user.username,
            'merchant_id': self.system.config.get('merchant_id', ''),
            'user_email': request.user.email,
        }
        return render(request, f'payment/{self.system.code}.html', context=context)

    def process_payment(self, request, params=None):
        hash_list = [
            self.system.config.get('merchant_id', ''),
            request.POST.get('AMOUNT', ''),
            self.system.config.get('secret_key2', ''),
            request.POST.get('MERCHANT_ORDER_ID', ''),
        ]
        signature = self.create_signature(hash_list)
        if signature == request.POST.get('SIGN', ''):
            self.transaction_id = request.POST.get('MERCHANT_ORDER_ID', '')
            self.set_transaction(self.transaction_id)
            if self.transaction and self.transaction.status_id == PaymentStatus.PROCESS:
                received_data = self.get_json_post_data(request)
                params = {'response': 'YES'}
                Mailer.send_managers('successful_payment', f'Received successful payment from - {self.NAME}', {
                    'received_data': received_data,
                    'payment_system': {self.NAME},
                })
                return super(FreekassaPayment, self).process_payment(request, params)
        return HttpResponse('ERROR')
