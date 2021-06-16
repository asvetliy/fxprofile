from django.apps import apps


Prices = apps.get_model('mt4', 'Prices')
Currency = apps.get_model('currency', 'Currency')
