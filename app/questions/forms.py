from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CreateTicketForm(forms.Form):
    ticket_text = forms.CharField(
        widget=forms.Textarea,
        max_length=300,
        min_length=1
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )
