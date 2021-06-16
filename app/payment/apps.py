from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        from .updater import Updater
        Updater.start()
