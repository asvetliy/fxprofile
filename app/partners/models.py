from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()
Transaction = apps.get_model('wallet', 'Transaction', require_ready=False)
Wallet = apps.get_model('wallet', 'Wallet', require_ready=False)
Verification = apps.get_model('verification', 'Verification', require_ready=False)
VerificationRequest = apps.get_model('verification', 'VerificationRequest', require_ready=False)
Card = apps.get_model('verification', 'Card', require_ready=False)


class PartnerUser(User):

    class Meta:
        proxy = True


class PartnerTransaction(Transaction):

    class Meta:
        proxy = True
