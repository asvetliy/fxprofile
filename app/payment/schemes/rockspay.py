import json
import requests
import hmac
import hashlib

from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.utils import timezone

from json_logging import log
from mailer import Mailer

from .base import BaseScheme, ftos
from ..constants import ROCKSPAY_CURRENCIES


class RockspayPayment(BaseScheme):
    API_URL = 'https://api.rockspay.ru'
    CREATE_INVOICE_URL = API_URL + '/v1/p2p/payments/invoice'

    def generate_signature(self, data: list) -> str:
        hashable_str = ''.join(map(str, data))
        log.info(f'hashable_str = {hashable_str}')
        return hmac.new(self.system.config.get('secret_key', '').encode('utf-8'), hashable_str.encode('utf-8'),
                        hashlib.sha512).hexdigest()

    def rockspay_init(self, request):
        t = int(timezone.now().timestamp())
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
                return redirect(f"https://rockspay.net/checkout?guid={response['value'].get('guid', None)}", permanent=True)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _('PAYMENT_ROCKSPAY_FAIL_STATUS_CODE') % init_response.status_code,
            )
            return redirect('wallet-deposit')

    def process_payment(self, request, params=None):
        callback = json.loads(request.body)
        signature = callback.get('Signature', None)
        if signature == self.generate_signature([
            callback['Data'].get('Guid', ''),
            callback['Data'].get('Status', ''),
            callback['Data'].get('InvoiceNumber', ''),
            callback['Data'].get('Currency', ''),
            ftos(callback['Data'].get('Amount', '')),
            callback['Data'].get('AccountNumber', ''),
            callback['Data'].get('Duration', ''),
            callback['Data'].get('Nonce', ''),
        ]):
            callback_type = callback.get('Type', None)
            transaction_id = int(callback['Data'].get('InvoiceNumber', ''))
            self.set_transaction_by_id(transaction_id)
            if self.transaction:
                if callback_type in (1, 2, ):
                    return HttpResponse('')
                if callback_type == 3:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 1
                        self.transaction.save()
                        Mailer.send_managers('successful_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
                if callback_type == 4:
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 4
                        self.transaction.save()
                        Mailer.send_managers('failed_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
                if callback_type in (5, 6, ):
                    if self.transaction.status_id == 2:
                        self.transaction.status_id = 6
                        self.transaction.save()
                        Mailer.send_managers('failed_payment', f'Received callback from - {self.system.code}', {
                            'received_data': json.dumps(callback),
                            'payment_system': self.system.code,
                        })
        return HttpResponse('')
