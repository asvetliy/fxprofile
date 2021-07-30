from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Transaction
from .helpers import int_to_amount, amount_to_int


class TransactionAdminForm(forms.ModelForm):
    transaction_amount = forms.FloatField(required=True, localize=True)
    _is_new: bool

    def __init__(self, *args, **kwargs):
        self._is_new = kwargs.get('instance') is None
        super(TransactionAdminForm, self).__init__(*args, **kwargs)
        if not self._is_new:
            self.fields['transaction_amount'].initial = int_to_amount(
                self.instance.amount,
                self.instance.wallet.currency.digest
            )

    def save(self, commit=True):
        if 'transaction_amount' in self.changed_data:
            self.instance.amount = amount_to_int(
                self.cleaned_data.get('transaction_amount'),
                self.instance.wallet.currency.digest
            )
        return super(TransactionAdminForm, self).save(commit=commit)

    class Meta:
        model = Transaction
        fields = '__all__'


class WithdrawForm(forms.Form):
    amount = forms.FloatField(min_value=0, required=True)
    account = forms.IntegerField(min_value=0, required=True)
    payment_system = forms.CharField(min_length=1, required=True)
    to_wallet = forms.CharField(max_length=32, required=True)


class TransferForm(forms.Form):
    amount = forms.FloatField(min_value=0, required=True)
    transfer_type = forms.CharField(required=True)
    from_personal_account = forms.IntegerField(min_value=1, required=False)
    from_trading_account = forms.IntegerField(min_value=1, required=False)
    to_personal_account = forms.IntegerField(min_value=1, required=False)
    to_trading_account = forms.IntegerField(min_value=1, required=False)

    def clean_transfer_type(self):
        transfer_type = self.cleaned_data.get('transfer_type')
        if transfer_type == 'pt':
            from_account = int(self.data['from_personal_account'])
            to_account = int(self.data['to_trading_account'])
        elif transfer_type == 'tp':
            from_account = int(self.data['from_trading_account'])
            to_account = int(self.data['to_personal_account'])
        else:
            raise forms.ValidationError('Wrong transfer type')

        if from_account > 0 and to_account > 0:
            self.cleaned_data['from_account'] = from_account
            self.cleaned_data['to_account'] = to_account
            self.cleaned_data['transfer_code'] = transfer_type
        else:
            raise forms.ValidationError(_('WALLET_FORM_ERROR_WRONG_FROMTO_ACCOUNTS'))
