from .models import Prices


class Exchange(object):
    @staticmethod
    def conv(amount: float, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return amount
        symbol = from_currency + to_currency
        price = Prices.objects.get(SYMBOL=symbol)
        if price:
            return price.ASK * amount
        else:
            symbol = to_currency + from_currency
            price = Prices.objects.get(SYMBOL=symbol)
            if price:
                return (1 / price.ASK) * amount
        return amount

