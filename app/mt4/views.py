from django.views import View
from django.views.defaults import page_not_found
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.db import connection
from django.conf import settings
from django.urls import reverse

from .models import UserAccounts, Trades, Accounts
from .server import Mt4Server, AccountObject
from .forms import *


def dictfetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_free_account_id():
    last = Accounts.objects.order_by('-LOGIN').filter(
        LOGIN__lt=settings.MT4_ACCOUNTS_SETTINGS['MT4_REAL']['TO'],
        LOGIN__gt=settings.MT4_ACCOUNTS_SETTINGS['MT4_REAL']['FROM']
    ).first()
    if last is None:
        return settings.MT4_ACCOUNTS_SETTINGS['MT4_REAL']['FROM']

    return last.LOGIN + settings.MT4_ACCOUNTS_SETTINGS['MT4_REAL']['STEP']


class TradingURLDispatcher(LoginRequiredMixin, View):
    def post(self, request, account, action):
        return page_not_found(request, None)

    def get(self, request, account, action):
        if action == 'view':
            if not request.user.useraccounts_set.filter(pk=account).exists():
                return page_not_found(request, None)
            user_account = request.user.useraccounts_set.get(id=account)
            mt4_account = Accounts.objects.get(LOGIN=account)
            trades = Trades.objects.filter(LOGIN=account).order_by('TICKET')
            pl_chart_data, tmp, dwp_pie_deposits, dwp_pie_withdraws, i, profit = '[0,0],', 0, 0, 0, 1, 0
            dwp_pie_own_money, dwp_pie_profit, dwp_pie_nomoney = 0, 0, 100
            for trade in trades:
                if trade.CMD in (1, 2, ) and trade.CLOSE_TIME != '1970-01-01 00:00:00':
                    profit += trade.PROFIT
                if trade.DIGITS > 0:
                    tmp += trade.PROFIT
                    pl_chart_data += f"['{i}',{tmp}],"
                    i += 1
                if trade.CMD == 6:
                    if trade.PROFIT > 0:
                        dwp_pie_deposits += trade.PROFIT
                    else:
                        dwp_pie_withdraws += (trade.PROFIT * -1)
            if mt4_account.BALANCE > 0:
                dwp_pie_dp = dwp_pie_deposits - dwp_pie_withdraws
                dwp_pie_nomoney = 0
                if dwp_pie_dp <= 0:
                    dwp_pie_own_money = 0
                    dwp_pie_profit = 100
                else:
                    dwp_pie_own_money = round((dwp_pie_dp * 100) / mt4_account.BALANCE, 2)
                    dwp_pie_profit = 100 - dwp_pie_own_money
            context = {
                'title_category': _('MT4_ACCOUNT_VIEW_TITLE'),
                'nav_acc_view': 'active',
                'nav_acc_collapsed': 'show',
                'nav_acc_management': 'active',
                'trades': trades,
                'pl_chart_data': pl_chart_data,
                'user_account': user_account,
                'mt4_account': mt4_account,
                'profit': profit,
                'dwp_pie_own_money': dwp_pie_own_money,
                'dwp_pie_profit': dwp_pie_profit,
                'dwp_pie_nomoney': dwp_pie_nomoney,
                'current_url': reverse('mt4-account-action', args=(account, action))
            }
            return render(request, 'mt4/view-account.html', context=context)
        return page_not_found(request, None)


class CreateAccountView(LoginRequiredMixin, View):
    leverages = (500, 400, 300, 200, 100, 50)

    def get(self, request):
        context = {
            'nav_acc_registration': 'active',
            'nav_acc_collapsed': 'show',
            'nav_acc_management': 'active',
            'title_category': _('MT4_ACCOUNT_REG_TITLE'),
            'leverages': self.leverages,
            'form': CreateAccountForm()
        }
        return render(request, 'mt4/create-account.html', context=context)

    def post(self, request):
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            mt4 = Mt4Server()
            account_obj = AccountObject()
            account_obj.from_user(user=request.user)
            account_obj.account_id = str(get_free_account_id())
            account_obj.leverage = str(form.cleaned_data['account_leverage'])
            account_obj.group_id = \
            settings.MT4_ACCOUNTS_SETTINGS['MT4_REAL']['GROUPS'][form.cleaned_data['account_currency']][
                form.cleaned_data['account_type']]
            account_id = mt4.create_account(account_obj)
            if account_id and account_id.isdigit():
                currency_id = form.cleaned_data.get('account_currency', 1)
                UserAccounts.objects.create(
                    user=request.user,
                    is_pamm=False,
                    id=account_id,
                    account_type_id=form.cleaned_data['account_type'],
                    pwd=account_obj.user_pwd,
                    phone_pwd=account_obj.phone_pwd,
                    inv_pwd=account_obj.inv_pwd,
                    currency_id=currency_id
                )
                messages.add_message(request, messages.SUCCESS, _('MT4_ACCOUNT_CREATE_SUCCESS'))
                return redirect('mt4-accounts')
        messages.add_message(request, messages.ERROR, _('MT4_ACCOUNT_CREATE_FAIL'))
        if form.errors:
            for k, e in form.error_messages.items():
                messages.add_message(request, messages.ERROR, e)
        return redirect('mt4-account-create')


class AccountsView(LoginRequiredMixin, View):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT a.id as id, b.REGDATE, b.BALANCE, b.CURRENCY, b.LEVERAGE, t.name as type
            FROM accounts as a, MT4_USERS as b, account_types as t
        WHERE a.id=b.LOGIN AND a.account_type_id=t.id AND a.user_id=%s
        """, [request.user.id])
        mt4_accounts = dictfetchall(cursor)

        context = {
            'title_category': _('MT4_ACCOUNTS_VIEW_TITLE'),
            'nav_acc_view': 'active',
            'nav_acc_collapsed': 'show',
            'nav_acc_management': 'active',
            'mt4_accounts': mt4_accounts,
        }
        return render(request, 'mt4/accounts.html', context=context)
