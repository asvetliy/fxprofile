from django.apps import AppConfig


class VerificationConfig(AppConfig):
    name = 'verification'

    def ready(self):
        from . import signals
