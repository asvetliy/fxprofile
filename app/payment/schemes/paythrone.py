import hmac
import hashlib

from django.shortcuts import render
from django.http import HttpResponse

from mailer import Mailer

from .base import BaseScheme
from ..constants import PaymentStatus


class PaythronePayment(BaseScheme):
    def init_payment(self, request):
        super(PaythronePayment, self).init_payment(request)
        description = 'Account replenishment'
        hash_list = [
            str(request.user.id),
            request.user.email,
            request.user.first_name + ' ' + request.user.last_name,
            self.system.config.get('public_key', ''),
            self.converted_amount_str,
            self.to_currency,
            str(self.transaction_id),
            description,
        ]
        hash_list.sort()
        hash_string = '|'.join(hash_list)
        signature = hmac.new(self.system.config.get('private_key', '').encode('utf-8'), hash_string.encode('utf-8'),
                             hashlib.sha256).hexdigest()
        context = {
            'signature': signature,
            'amount': self.converted_amount_str,
            'currency': self.to_currency,
            'description': description,
            'transaction_id': self.transaction_id,
            'username': request.user.first_name + ' ' + request.user.last_name,
            'project': self.system.config.get('public_key', ''),
            'user_id': request.user.id,
            'user_email': request.user.email,
            'user_name': request.user.first_name + ' ' + request.user.last_name,
        }

        return render(request, f'payment/{self.system.code}.html', context=context)

    def process_payment(self, request, params=None):
        self.transaction_id = request.POST['order_id']
        self.set_transaction(self.transaction_id)
        if self.transaction and self.transaction.status_id == PaymentStatus.PROCESS:
            received_data = self.get_json_post_data(request)
            if request.POST['status'] == 'completed':
                params = {'response': 'OK'}
                Mailer.send_managers('successful_payment', 'Received successful payment from - Paythrone', {
                    'received_data': received_data,
                    'payment_system': 'Paythrone',
                })
                return super(PaythronePayment, self).process_payment(request, params)
            elif request.POST['status'] == 'failed':
                Mailer.send_managers('failed_payment', 'Received failed payment from - Paythrone', {
                    'received_data': received_data,
                    'payment_system': 'Paythrone',
                })
                return HttpResponse('OK')
        return HttpResponse('ERROR')
