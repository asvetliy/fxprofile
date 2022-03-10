from django.urls import path

from . import views

urlpatterns = [
    path('trading/account/create', views.CreateAccountView.as_view(), name='mt4-account-create'),
    path('trading/accounts', views.AccountsView.as_view(), name='mt4-accounts'),
    path('trading/<int:account>/<str:action>', views.TradingURLDispatcher.as_view(), name='mt4-account-action'),
]
