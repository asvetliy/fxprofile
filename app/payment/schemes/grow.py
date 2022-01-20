import json
import requests
import hashlib

from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from json_logging import log
from mailer import Mailer

from .base import BaseScheme


class GrowPayment(BaseScheme):
    CREATE_INVOICE_PATH = '/api/v5/invoice/get'

    def __init__(self, payment_system):
        super().__init__(payment_system)
        self.sandbox_enabled = self.system.config.get('sandbox_enabled', False)
        if self.sandbox_enabled:
            self.api_url = self.system.config.get('sandbox_api_url', '')
        else:
            self.api_url = self.system.config.get('api_url', '')
        self.merchant_id = self.system.config.get('merchant_id', '')
        self.return_url = self.system.config.get('return_url', '')
        self.response_url = self.system.config.get('response_url', '')
        self.server_url = self.system.config.get('server_url', '')
        self.cancel_url = self.system.config.get('cancel_url', '')
        self.api5_key = self.system.config.get('api5_key', '')
        self.exact_currency = self.system.config.get('exact_currency', 0)

    def generate_signature(self, hash_list: list) -> str:
        hash_list.sort()
        hash_string = '|'.join(map(str, hash_list))
        hash_string = self.api5_key + '|' + hash_string
        log.info(hash_string)
        return hashlib.sha1(hash_string.encode('utf-8')).hexdigest().lower()

    def grow_init(self, init_data):
        return requests.post(self.api_url + self.CREATE_INVOICE_PATH, headers={
            'Authorization': f'Bearer {self.api5_key}',
            'content-type': 'application/json',
        }, json=init_data)

    def init_payment(self, request):
        super(GrowPayment, self).init_payment(request)
        init_response = self.grow_init({
            'order_id': self.transaction_id,
            'amount': self.converted_amount,
            'currency': self.to_currency,
            'return_url': self.return_url,
            'response_url': self.response_url,
            'cancel_url': self.cancel_url,
            'server_url': self.server_url,
            'exact_currency': self.exact_currency,
        })
        if init_response.status_code == 200:
            response = init_response.json()
            status = response.get('status', None)
            if not status:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{response.get('message', None)}",
                )
                return redirect('wallet-deposit')
            else:
                return redirect(f"{response.get('url', None)}", permanent=True)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _('PAYMENT_GROW_FAIL_STATUS_CODE') % init_response.status_code,
            )
            return redirect('wallet-deposit')

    def process_payment(self, request, params=None):
        callback = request.POST
        signature = callback.get('signature', None)
        log.info(callback)
        new_signature = self.generate_signature([
            self.merchant_id,
            callback.get('invoice_id', ''),
            callback.get('order_id', ''),
            callback.get('amount', ''),
            callback.get('amount_currency', ''),
            callback.get('currency', ''),
            callback.get('merchant_amount', ''),
            callback.get('account_info', ''),
            callback.get('status', ''),
        ])
        if signature == new_signature:
            callback_type = int(callback.get('status', None))
            transaction_id = int(callback.get('order_id'))
            self.set_transaction_by_id(transaction_id)
            if self.transaction:
                if callback_type not in (1, 0, -1, ):
                    return HttpResponse('')
                if callback_type == 1:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 1
                        self.transaction.save()
                        Mailer.send_managers('successful_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
                if callback_type == 0:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 4
                        self.transaction.save()
                        Mailer.send_managers('failed_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
                if callback_type == -1:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 6
                        self.transaction.save()
                        Mailer.send_managers('failed_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
        else:
            log.info('Wrong signature')
            log.info(f'{signature} != {new_signature}')
        return HttpResponse('')
