from django.apps import AppConfig
from django.conf import settings


class WalletConfig(AppConfig):
    name = 'wallet'

    def ready(self):
        from . import signals
        if not settings.DEBUG:
            from .updater import Updater
            Updater.start()
