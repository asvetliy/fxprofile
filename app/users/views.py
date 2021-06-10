from django.views import View
from django.contrib.auth import login, views as auth_views
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from mailer.utils import Mailer

from .tokens import account_activation_token
from .forms import *


class UserCreationView(View):
    def get(self, request):
        context = {
            'title': _('USERS_REG_TITLE'),
            'page': 'registration',
            'form': UserRegistrationForm()
        }
        return render(request, 'users/registration.html', context=context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            group = Group.objects.get(name='Registered')
            user.groups.add(group)
            user.save()

            current_site = get_current_site(request)
            Mailer.send('reg_email_confirm', user, subject=_('USERS_REG_EMAIL_CONFIRM_SUBJECT'), params={
                'domain': current_site.domain,
                'activation_url': reverse('activate', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }),
                'title': _('USERS_REG_EMAIL_CONFIRM_SUBJECT'),
            })
            return redirect('account-activation-sent')
        else:
            context = {
                'errors': form.error_messages,
                'title': _('USERS_REG_TITLE'),
                'page': 'registration',
                'form': form
            }
            return render(request, 'users/registration.html', context=context)


class UserLoginView(auth_views.LoginView):
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'
    # success_url = '/'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if 'login_count' not in self.request.session:
            request.session['login_count'] = 0

        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.session['login_count'] >= settings.RECAPTCHA_LOGIN_FAILED_TRIES:
            context['captcha'] = True
            context['form'].fields['captcha'] = ReCaptchaField(
                widget=ReCaptchaWidget()
            )
        else:
            context['captcha'] = False
        self.request.session['login_count'] += 1
        context['title'] = _('USER_LOGIN_PAGE_TITLE')
        return super(UserLoginView, self).render_to_response(context, **response_kwargs)


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile-index')
    else:
        return render(request, 'users/account_activation_invalid.html')


class UserPasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('user-password-reset-done')


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class UserPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('user-password-reset-complete')
    form_class = UserPasswordResetConfirmForm
