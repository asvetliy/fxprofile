from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration', views.UserCreationView.as_view(), name='user-reg'),
    path('login', views.UserLoginView.as_view(), name='user-login'),
    path('logout', auth_views.LogoutView.as_view(), name='user-logout'),
    path('account-activation-sent',
         auth_views.TemplateView.as_view(template_name='users/account_activation_sent.html'),
         name='account-activation-sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('password-reset', views.UserPasswordResetView.as_view(), name='user-password-reset'),
    path('password-reset/done', views.UserPasswordResetDoneView.as_view(), name='user-password-reset-done'),
    path('password-reset/<uidb64>/<token>/', views.UserPasswordResetConfirm.as_view(), name='user-password-reset-confirm'),
    path('password-reset/complete', views.UserPasswordResetComplete.as_view(), name='user-password-reset-complete'),
]
