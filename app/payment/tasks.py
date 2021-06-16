from django.utils import timezone

from .models import Transaction, BlockchainWallet


def close_expired_blockchain_transactions():
    wallets = BlockchainWallet.objects.filter(expired_at__lte=timezone.now())
    for w in wallets:
        if w.transaction is not None:
            t = w.transaction  # type: Transaction
            t.status_id = 4
            t.save()
        w.expired_at = None
        w.picked_at = None
        w.transaction = None
        w.save()
