from django.urls import path
from . import views

urlpatterns = [
    path('deposit', views.WalletDepositView.as_view(), name='wallet-deposit'),
    path('withdraw', views.WalletWithdrawView.as_view(), name='wallet-withdraw'),
    path('transfer', views.WalletTransferView.as_view(), name='wallet-transfer'),
    path('history', views.WalletHistoryView.as_view(), name='wallet-history'),
]
