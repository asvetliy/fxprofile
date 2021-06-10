from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, \
    SetPasswordForm
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth import password_validation
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from .models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    country = CountryField().formfield(widget=CountrySelectWidget(
        attrs={'class': 'form-control selectpicker', 'data-style': 'btn btn-link'},
        layout='{widget}<img class="img-country-flag" id="{flag_id}" src="{country.flag}">'
    ))
    first_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    city = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('USERS_PHONE_VALIDATION_ERROR')
    )
    phone = forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=17,
        required=True
    )
    promo = forms.CharField(
        required=False,
        max_length=64,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'email', 'password1', 'password2',
            'country', 'city', 'phone',
            'promo', 'username', 'birth_date',
        ]


class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('USERS_LOGIN_FORM_USERNAME')}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('USERS_LOGIN_FORM_PWD')}),
    )

    def __init__(self, request, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(request, *args, **kwargs)
        if self.request.session.get('login_count', 0) > settings.RECAPTCHA_LOGIN_FAILED_TRIES:
            self.fields['captcha'] = ReCaptchaField(
                widget=ReCaptchaWidget()
            )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=None,
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': _('USERS_RESET_FORM_EMAIL')})
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )


class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=None,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': _('USERS_RESET_FORM_NEW_PWD')}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=None,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': _('USERS_RESET_FORM_NEW_PWD2')}),
    )
