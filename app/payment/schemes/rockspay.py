import json
import requests
import hmac
import hashlib

from time import time

from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.utils import timezone

from mailer import Mailer

from .base import BaseScheme
from ..constants import ROCKSPAY_CURRENCIES


class RockspayPayment(BaseScheme):
    NAME = 'Rockspay'
    API_URL = 'https://api.rockspay.ru'
    CREATE_INVOICE_URL = API_URL + '/v1/p2p/payments/invoice'
    CHECK_INVOICE_URL = API_URL + '/v1/p2p/payments/invoice/%s/check'

    def generate_signature(self, data: list) -> str:
        hashable_str = ''.join(map(str, data))
        return hmac.new(self.system.config.get('secret_key', '').encode('utf-8'), hashable_str.encode('utf-8'),
                        hashlib.sha512).hexdigest()

    def rockspay_init(self, request):
        t = int(time())
        return requests.post(self.CREATE_INVOICE_URL, headers={
            'MERCHANT': self.system.config.get('merchant_id', ''),
            'SIGNATURE': self.generate_signature([
                self.transaction_id,
                ROCKSPAY_CURRENCIES.get(self.to_currency),
                self.converted_amount_str,
                t,
            ]),
            'Content-Type': 'application/json',
        }, json={
            "invoiceNumber": str(self.transaction_id),
            "country": request.user.country.code.lower(),
            "accountType": 1,
            "senderDetails": request.POST.get('card_number', ''),
            "currency": ROCKSPAY_CURRENCIES.get(self.to_currency),
            "amount": self.converted_amount_str,
            "comment": "",
            "duration": self.system.config.get('duration', 3600),
            "callbackUrl": self.system.config.get('callback_url', ''),
            "nonce": t,
        })

    def rockspay_check(self, request):
        invoice_id = request.GET.get('invoice_id', None)
        if invoice_id:
            return requests.get(self.CHECK_INVOICE_URL % invoice_id, headers={
                'MERCHANT': self.system.config.get('merchant_id', ''),
                'SIGNATURE': self.generate_signature([
                    invoice_id,
                ]),
                'Content-Type': 'application/json',
            }).json()
        return None

    def init_payment(self, request):
        super(RockspayPayment, self).init_payment(request)
        init_response = self.rockspay_init(request)
        if init_response.status_code == 200:
            response = init_response.json()
            if response.get('isFailure', None):
                for msg in response.get('failures'):
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"{msg.get('id', '')} - {msg.get('description', '')}",
                    )
                return redirect('wallet-deposit')
            if response.get('isSuccess', None):
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
                    'payment_system_data': response,
                }, indent=2)
                Mailer.send_managers('successful_payment', f'Received initial payment from - {self.NAME}', {
                    'received_data': received_data,
                    'payment_system': self.NAME,
                })
                context = {
                    'amount': self.converted_amount_str,
                    'currency': self.to_currency,
                    'card_number': response['value'].get('accountNumber', None),
                    'expired_at': response['value'].get('duration', 3600) + int(timezone.now().timestamp()),
                    'invoice_id': response['value'].get('guid', None),
                }
                return render(request, f'payment/{self.system.code}.html', context=context)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _('PAYMENT_ROCKSPAY_FAIL_STATUS_CODE') % init_response.status_code,
            )
            return redirect('wallet-deposit')

    def process_payment(self, request, params=None):
        callback = json.loads(request.body)
        signature = callback.get('signature', None)
        if signature == self.generate_signature([
            callback['data'].get('guid', ''),
            callback['data'].get('status', ''),
            callback['data'].get('invoiceNumber', ''),
            callback['data'].get('currency', ''),
            callback['data'].get('amount', ''),
            callback['data'].get('accountNumber', ''),
            callback['data'].get('duration', ''),
            callback['data'].get('nonce', ''),
        ]):
            callback_type = callback.get('type', None)
            if callback_type == 3:
                self.set_transaction_by_id(callback['data'].get('invoiceNumber', ''))
                if self.transaction:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 1
                        self.transaction.save()
            if callback_type == 4:
                self.set_transaction_by_id(callback['data'].get('invoiceNumber', ''))
                if self.transaction:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 4
                        self.transaction.save()
            if callback_type == (5, 6, ):
                self.set_transaction_by_id(callback['data'].get('invoiceNumber', ''))
                if self.transaction:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 6
                        self.transaction.save()
        Mailer.send_managers('successful_payment', f'Received callback from - {self.NAME}', {
            'received_data': json.dumps(callback),
            'payment_system': self.NAME,
        })
        return HttpResponse('')

    def check_payment(self, request):
        response = self.rockspay_check(request)
        if response:
            if response.get('isSuccess', None):
                return redirect('/payments/rockspay/success')
            elif response.get('isFailure', None):
                for msg in response.get('failures'):
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"{msg.get('id', '')} - {msg.get('description', '')}",
                    )
                return redirect('/payments/rockspay/fail')
        return redirect('/payments/rockspay/fail')

    def success_payment(self, request):
        return render(request, 'payment/wait_payment.html')
