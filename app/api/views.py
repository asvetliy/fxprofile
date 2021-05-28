from rest_framework import generics
from django.apps import apps

from .serializer import PricesSerializer

Prices = apps.get_model('mt4', 'Prices')


class PricesList(generics.ListAPIView):
    model = Prices
    serializer_class = PricesSerializer
    queryset = Prices.objects.all()

    def get_queryset(self):
        queryset = super(PricesList, self).get_queryset()
        symbols = self.request.query_params.get('symbols', None)
        if symbols:
            return queryset.filter(SYMBOL__in=symbols.split(','))
        return queryset
