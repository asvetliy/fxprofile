from .models import Prices


def get_price_or_none(model: Prices, *args, **kwargs):
    try:
        return Prices.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class Exchange(object):
    @staticmethod
    def conv(amount: float, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return amount
        symbol = from_currency + to_currency
        price = get_price_or_none(Prices, SYMBOL=symbol)
        if price:
            return price.ASK * amount
        else:
            symbol = to_currency + from_currency
            price = get_price_or_none(Prices, SYMBOL=symbol)
            if price:
                return (1 / price.ASK) * amount
        return amount

