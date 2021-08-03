from django import forms

from math_helper import int_to_amount

from .models import Transaction


class PartnerTransactionAdminForm(forms.ModelForm):
    transaction_amount = forms.FloatField(required=True, localize=True, label='Amount')
    _is_new: bool

    def __init__(self, *args, **kwargs):
        self._is_new = kwargs.get('instance') is None
        super(PartnerTransactionAdminForm, self).__init__(*args, **kwargs)
        if not self._is_new:
            self.fields['transaction_amount'].initial = int_to_amount(
                self.instance.amount,
                self.instance.wallet.currency.digest
            )

    class Meta:
        model = Transaction
        fields = ['transaction_amount', 'wallet', 'user', 'from_to_wallet', 'type', 'status', 'description', ]
        readonly_fields = ['created_at']
