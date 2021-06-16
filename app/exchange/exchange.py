from .models import Prices, Currency


def get_price_or_none(*args, **kwargs):
    try:
        return Prices.objects.get(*args, **kwargs)
    except Prices.DoesNotExist:
        return None


class Exchange(object):
    def conv(self, amount: float, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return amount
        symbol = from_currency + to_currency
        price = get_price_or_none(SYMBOL=symbol)
        if price:
            return price.ASK * amount
        else:
            symbol = to_currency + from_currency
            price = get_price_or_none(SYMBOL=symbol)
            if price:
                return (1 / price.ASK) * amount
        # try double covert
        try:
            base_currency = Currency.objects.get(is_base=True)
        except Currency.DoesNotExist:
            return 0
        convert_to_base_amount = self.conv(amount, from_currency, base_currency.iso)
        if convert_to_base_amount:
            return self.conv(convert_to_base_amount, base_currency.iso, to_currency)
        return 0

