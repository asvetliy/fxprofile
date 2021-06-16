from datetime import timedelta
from math import ceil

from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .base import BaseScheme, itos
from ..models import BlockchainWallet


class BlockchainPayment(BaseScheme):
    NAME = 'Blockchain'

    def init_payment(self, request):
        blockchain_wallet = BlockchainWallet.objects.filter(
            transaction__user__id=request.user.id,
            expired_at__gte=timezone.now() - timedelta(minutes=1)
        ).first()  # type: BlockchainWallet
        if not blockchain_wallet:
            blockchain_wallet = BlockchainWallet.objects.filter(transaction=None).first()
            if not blockchain_wallet:
                messages.add_message(request, messages.ERROR, _('PAYMENT_BLOCKCHAIN_NO_EMPTY_WALLET'))
                return redirect('wallet-deposit')
            super(BlockchainPayment, self).init_payment(request)
            picked_at = timezone.now()
            expired_at = picked_at + timedelta(seconds=self.system.config.get('expire_time', 60*5))
            blockchain_wallet.transaction = self.transaction
            blockchain_wallet.expired_at = expired_at
            blockchain_wallet.picked_at = picked_at
            blockchain_wallet.save()
        else:
            self.set_transaction(blockchain_wallet.transaction)
            super(BlockchainPayment, self).init_payment(request)
        context = {
            'blockchain_wallet': blockchain_wallet.bwallet,
            'amount': itos(self.int_amount, self.wallet.currency.digest),
            'currency': self.from_currency,
            'converted_currency': self.to_currency,
            'transaction_id': self.transaction_id,
            'converted_amount': self.converted_amount_str,
            'expired_at': ceil(blockchain_wallet.expired_at.timestamp()),
        }
        return render(request, f'payment/{self.system.code}.html', context=context)

    def process_payment(self, request, params: dict = None):
        return HttpResponse('')
