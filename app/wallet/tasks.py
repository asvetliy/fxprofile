from datetime import datetime

from .models import Transaction


def close_expired_transactions():
    current_transactions = Transaction.objects.filter(status_id=2)
    for transaction in current_transactions:
        duration = datetime.now().timestamp() - transaction.created_at.timestamp()
        if duration > 86400:
            transaction.status_id = 4
            transaction.save()
