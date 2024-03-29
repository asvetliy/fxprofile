from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from mailer.utils import Mailer

from .models import UserAccounts
from .server import Mt4Server, AccountObject

Transaction = apps.get_model('wallet', 'Transaction')


def change_balance(instance, description):
    mt4_server = Mt4Server()
    account_object = AccountObject()
    account_object.user_ip = instance.user_ip if hasattr(instance, 'user_ip') else ''
    account_object.account_id = str(instance.from_to_wallet)
    result = mt4_server.change_balance(
        account_object,
        str(float(instance.transaction_amount) * -1),
        description
    )
    if result:
        instance.status_id = 1
        instance.save()


@receiver(post_save, sender=UserAccounts)
def create_trading_account(sender, instance, created, **kwargs):
    if created:
        Mailer.send('trading_account_created', instance.user, subject=_('MT4_ACCOUNT_CREATE_EMAIL_SUBJECT'), params={
            'account_id': instance.id,
            'pwd': instance.pwd,
            'inv_pwd': instance.inv_pwd,
        })
        Mailer.send_managers('mt4_account_created', subject=f'User, {instance.user.username}, created an trading account', params={
            'user': instance.user,
            'account_id': instance.id,
        })


@receiver(post_save, sender=Transaction)
def transfer_funds(sender, instance, created, **kwargs):
    if created:
        if instance.type_id == 5:  # transfer_out
            change_balance(instance, 'transfer from personal')
    else:
        if 'status' in instance.changed_data and instance.changed_data['status'].id == 2 and instance.status_id == 1:
            if instance.type_id == 4:  # transfer_in
                change_balance(instance, 'transfer to personal')

