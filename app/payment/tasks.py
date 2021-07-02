from django.utils import timezone

from .models import Transaction, BlockchainWallet


def close_expired_blockchain_transactions():
    wallets = BlockchainWallet.objects.filter(expired_at__lte=timezone.now(), is_used=False)
    for w in wallets:
        if w.transaction is not None:
            if w.transaction.status_id == 2:
                w.transaction.status_id = 4
                w.transaction.save()
                w.expired_at = None
                w.picked_at = None
                w.transaction = None
                w.save()
            else:
                w.is_used = True
                w.save()
        else:
            w.expired_at = None
            w.picked_at = None
            w.transaction = None
            w.save()
