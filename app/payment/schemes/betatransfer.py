import hashlib
import requests

from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from mailer import Mailer

from .base import BaseScheme
from ..constants import PaymentStatus


class BetatransferPayment(BaseScheme):
    CREATE_INVOICE_URL = 'https://merchant.betatransfer.io/api/payment'

    @staticmethod
    def create_signature(hash_list: list):
        hash_string = ''.join(hash_list)
        return hashlib.md5(hash_string.encode('utf-8')).hexdigest()

    def betatransfer_init(self):
        return requests.post(f'{self.CREATE_INVOICE_URL}?token={self.system.config.get("public_key", "")}', headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        }, data={
            'amount': self.converted_amount_str,
            'currency': self.to_currency.lower(),
            'orderId': str(self.transaction_id),
            'paymentSystem': self.system.config.get('payment_method', ''),
            'urlSuccess': 'https://ca.xyz.trading/payments/betatransfer/success',
            'urlFail': 'https://ca.xyz.trading/payments/betatransfer/fail',
            'urlResult': 'https://ca.xyz.trading/payments/betatransfer/process',
            'sign': self.create_signature([
                self.converted_amount_str,
                self.to_currency.lower(),
                str(self.transaction_id),
                self.system.config.get('payment_method', ''),
                'https://ca.xyz.trading/payments/betatransfer/success',
                'https://ca.xyz.trading/payments/betatransfer/fail',
                'https://ca.xyz.trading/payments/betatransfer/process',
                self.system.config.get('secret', ''),
            ]),
        })

    def init_payment(self, request):
        # log.info(request)
        super(BetatransferPayment, self).init_payment(request)
        init_response = self.betatransfer_init()
        response = init_response.json()
        if init_response.status_code == 200:
            if response.get('status', None) == 'success':
                return redirect(response.get('url', None), permanent=True)
        elif init_response.status_code == 422:
            if 'errors' in response:
                for key, value in response['errors'].items():
                    messages.add_message(request, messages.ERROR, f"{key} - {value}")
                return redirect('wallet-deposit')
        messages.add_message(
            request,
            messages.ERROR,
            _('PAYMENT_BETATRANSFER_NOT_AVAILABLE'),
        )
        return redirect('wallet-deposit')

    def process_payment(self, request, params=None):
        signature = self.create_signature([
            request.POST.get('amount', ''),
            request.POST.get('orderId', ''),
            self.system.config.get('secret', ''),
        ])
        if signature == request.POST.get('sign', ''):
            self.transaction_id = request.POST.get('orderId', '')
            self.set_transaction_by_id(self.transaction_id)
            if self.transaction and self.transaction.status_id == PaymentStatus.PROCESS:
                received_data = self.get_json_post_data(request)
                Mailer.send_managers('successful_payment', f'Received successful payment from - {self.system.code}', {
                    'received_data': received_data,
                    'payment_system': {self.system.code},
                })
                self.transaction.status_id = PaymentStatus.DONE
                self.transaction.save()
                return HttpResponse('OK')
        return HttpResponse('ERROR')
