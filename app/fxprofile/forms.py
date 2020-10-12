from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django_countries.widgets import CountrySelectWidget
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(
        max_length=64,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    country = CountryField().formfield(widget=CountrySelectWidget(
        attrs={'class': 'form-control selectpicker', 'data-style': 'btn btn-link'},
        layout='{widget}<img class="img-country-flag" id="{flag_id}" src="{country.flag}">'
    ))
    email = forms.EmailField(
        max_length=128,
        disabled=True,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    last_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    city = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('PROFILE_PHONE_VALIDATION_ERROR')
        # message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
    )
    phone = forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=17,
        required=False
    )
    promo = forms.CharField(
        required=False,
        max_length=64,
        disabled=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'country', 'city', 'phone', 'username'
        ]


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100', 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )
