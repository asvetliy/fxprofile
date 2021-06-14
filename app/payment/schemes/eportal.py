from django.http import HttpResponse
from django.shortcuts import render

from .base import BaseScheme
from ..models import EportalWallets


class EportalPayment(BaseScheme):
    NAME = 'Eportal'

    def init_payment(self, request):
        super(EportalPayment, self).init_payment(request)
        try:
            eportal_wallet = EportalWallets.objects.get(user=request.user)
        except EportalWallets.DoesNotExist:
            eportal_wallet = EportalWallets.objects.filter(user=None).first()
            eportal_wallet.user = request.user
            eportal_wallet.save()
        context = {
            'eportal_wallet': eportal_wallet.ewallet,
            'amount': self.str_amount,
            'currency': self.to_currency,
            'transaction_id': self.transaction_id,
            'merchant_id': self.system.config.get('merchant_id', ''),
        }
        return render(request, f'payment/{self.system.code}.html', context=context)

    def process_payment(self, request, params: dict = None):
        return HttpResponse('')
