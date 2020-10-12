from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CreateAccountForm(forms.Form):
    account_type = forms.IntegerField(min_value=1)
    account_leverage = forms.IntegerField(min_value=1, max_value=1000)
    account_currency = forms.IntegerField(min_value=1)
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )
