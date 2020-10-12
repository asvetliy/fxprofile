from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .forms import UserUpdateForm, UserPasswordChangeForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        context = {
            'nav_dashboard': 'active',
            'wallets': request.user.wallet_set.all(),
            'title_category': _('PROFILE_VIEW_TITLE')
        }
        return render(request, 'fxprofile/index.html', context=context)


class ChangeProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        context = {
            'nav_change_profile': 'active',
            'nav_profile_collapsed': 'show',
            'title_category': _('PROFILE_CHANGE_PROFILE_TITLE'),
            'form': form
        }
        return render(request, 'fxprofile/change-profile.html', context=context)

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('PROFILE_CHANGE_SAVED_SUCCESS'))
            return redirect('profile-change')

        for k, e in form.error_messages.items():
            messages.add_message(request, messages.ERROR, e)
        return redirect('profile-change')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserPasswordChangeForm(request.user)
        context = {
            'nav_change_password': 'active',
            'nav_profile_collapsed': 'show',
            'title_category': _('PROFILE_CHANGE_PWD_TITLE'),
            'form': form
        }
        return render(request, 'fxprofile/change-password.html', context=context)

    def post(self, request):
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, _('PROFILE_PASSWORD_CHANGED_SUCCESS'))
            return redirect('password-change')

        for k, e in form.error_messages.items():
            messages.add_message(request, messages.ERROR, e)
        return redirect('password-change')
