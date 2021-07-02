from django.apps import AppConfig
from django.conf import settings


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        if not settings.DEBUG:
            from .updater import Updater
            Updater.start()
