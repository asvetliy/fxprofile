from django.apps import AppConfig


class Mt4Config(AppConfig):
    name = 'mt4'

    def ready(self):
        from . import signals
