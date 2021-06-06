from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import Wallet, Transaction
from .forms import *
from .helpers import *

PaymentSystem = apps.get_model('payment', 'PaymentSystem')


class WalletDepositView(View, LoginRequiredMixin):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        payment_systems = PaymentSystem.objects.filter(is_enabled=True).order_by('position')
        context = {
            'nav_funds_deposit': 'active',
            'nav_funds_collapsed': 'show',
            'nav_funds': 'active',
            'wallets': wallets,
            'title_category': _('WALLET_DEPOSIT_PAGE_TITLE'),
            'payment_systems': payment_systems
        }
        return render(request, 'wallet/deposit.html', context=context)


class WalletWithdrawView(View, LoginRequiredMixin):
    def get(self, request):
        wallets = request.user.wallet_set.all()
        payment_systems = PaymentSystem.objects.filter(is_enabled=True, withdraw=True)
        context = {
            'nav_funds_collapsed': 'show',
            'nav_funds_withdraw': 'active',
            'nav_funds': 'active',
            'title_category': _('WALLET_WITHDRAW_PAGE_TITLE'),
            'payment_systems': payment_systems,
            'wallets': wallets
        }
        return render(request, 'wallet/withdraw.html', context=context)

    def post(self, request):
        form = WithdrawForm(request.POST)
        if form.is_valid():
            payment_system = PaymentSystem.objects.get(
                is_enabled=True,
                withdraw=True,
                code=form.cleaned_data.get('payment_system')
            )
            if payment_system:
                Transaction.objects.create(
                    amount=ftoi(form.cleaned_data.get('amount') * -1),
                    wallet_id=form.cleaned_data.get('account'),
                    from_to_wallet=form.cleaned_data.get('payment_system'),
                    type_id=2,
                    status_id=2,
                    description=_('WALLET_WITHDRAW_VIA_PAYMENT') % {'payment_name': payment_system.name}
                )
                messages.add_message(request, messages.SUCCESS, _('WALLET_WITHDRAW_CREATED_SUCCESSFULLY'))
                return redirect('wallet-history')

        messages.add_message(request, messages.ERROR, _('WALLET_WITHDRAW_ERROR_NOT_VALID'))
        for k, e in form.error_messages.items():
            messages.add_message(request, messages.ERROR, e)
        return redirect('wallet-withdraw')


class WalletTransferView(View, LoginRequiredMixin):
    def get(self, request):
        wallets = request.user.wallet_set.all()
        mt4_accounts = request.user.useraccounts_set.all()
        context = {
            'title_category': _('WALLET_TRANSFER_PAGE_TITLE'),
            'nav_funds_transfer': 'active',
            'nav_funds_collapsed': 'show',
            'nav_funds': 'active',
            'wallets': wallets,
            'mt4_accounts': mt4_accounts
        }
        return render(request, 'wallet/transfer.html', context=context)

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data.get('from_account')
            to_account = form.cleaned_data.get('to_account')
            transfer_type = form.cleaned_data.get('transfer_code')
            amount = form.cleaned_data.get('amount')

            if transfer_type == 'pt':
                try:
                    user_wallet = request.user.wallet_set.get(id=from_account)
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.ERROR, _('WALLET_WITHDRAW_ERROR_WALLET_NOTEXIST'))
                    return redirect('wallet-transfer')
                if user_wallet.has_amount(amount):
                    try:
                        mt4_account = request.user.useraccounts_set.get(id=to_account)
                    except ObjectDoesNotExist:
                        messages.add_message(request, messages.ERROR, _('WALLET_WITHDRAW_ERROR_ACCOUNT_NOTEXIST'))
                        return redirect('wallet-transfer')
                    if mt4_account.currency_id != user_wallet.currency_id:
                        messages.add_message(request, messages.ERROR,
                                             _('WALLET_WITHDRAW_ERROR_CANT_TRANSFER'))
                        return redirect('wallet-transfer')
                    tr = Transaction(
                        amount=ftoi(amount * -1),
                        user=request.user,
                        wallet_id=from_account,
                        from_to_wallet=to_account,
                        type_id=5,
                        status_id=2,
                        description=_('WALLET_TRANSFER_TO_TRADING_ACCOUNT') % {'account_id': mt4_account.id}
                    )
                    tr.user_ip = get_client_ip(request)
                    tr.save()
                else:
                    messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_INSUFFICIENT_FUNDS'))
                    return redirect('wallet-transfer')
            elif transfer_type == 'tp':
                try:
                    mt4_account = request.user.useraccounts_set.get(id=from_account)
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_ACCOUNT_NOTEXIST'))
                    return redirect('wallet-transfer')
                if mt4_account.has_amount(amount):
                    try:
                        user_wallet = request.user.wallet_set.get(id=to_account)
                    except ObjectDoesNotExist:
                        messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_WALLET_NOTEXIST'))
                        return redirect('wallet-transfer')
                    if mt4_account.currency_id != user_wallet.currency_id:
                        messages.add_message(request, messages.ERROR,
                                             _('WALLET_TRANSFER_ERROR_CANT_TRANSFER'))
                        return redirect('wallet-transfer')
                    tr = Transaction(
                        amount=ftoi(amount),
                        wallet_id=to_account,
                        user=request.user,
                        from_to_wallet=from_account,
                        type_id=4,
                        status_id=2,
                        description=_('WALLET_TRANSFER_FROM_TRADING_ACCOUNT') % {'account_id': mt4_account.id}
                    )
                    tr.user_ip = get_client_ip(request)
                    tr.save()
                else:
                    messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_INSUFFICIENT_FUNDS'))
                    return redirect('wallet-transfer')
            else:
                messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_NOT_VALID'))
                return redirect('wallet-transfer')

            messages.add_message(request, messages.SUCCESS, _('WALLET_TRANSFER_CREATED_SUCCESSFULLY'))
            return redirect('wallet-history')
        messages.add_message(request, messages.ERROR, _('WALLET_TRANSFER_ERROR_NOT_VALID'))
        for k, e in form.error_messages.items():
            messages.add_message(request, messages.ERROR, e)
        return redirect('wallet-transfer')


class WalletHistoryView(View, LoginRequiredMixin):
    def get(self, request):
        wallets = []
        for wallet in request.user.wallet_set.all():
            wallets.append({
                'wallet': wallet,
                'transactions': wallet.transaction_set.all()
            })
        context = {
            'title_category': _('WALLET_TRANSFER_HISTORY_PAGE_TITLE'),
            'nav_funds_history': 'active',
            'nav_funds_collapsed': 'show',
            'nav_funds': 'active',
            'wallets': wallets,
            'colors': ['table-success', 'table-info', 'table-danger', 'table-warning']
        }
        return render(request, 'wallet/history.html', context=context)
