from rest_framework import serializers
from django.apps import apps

Prices = apps.get_model('mt4', 'Prices')


class PricesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prices
        fields = ['SYMBOL', 'BID', 'ASK', 'DIRECTION', 'SPREAD']
