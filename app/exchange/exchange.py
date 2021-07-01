from .models import Prices, Currency


def get_price_or_none(*args, **kwargs):
    try:
        return Prices.objects.get(*args, **kwargs)
    except Prices.DoesNotExist:
        return None


class Exchange(object):
    def conv(self, amount: float, from_currency: str, to_currency: str, rounding: bool = False) -> float:
        if from_currency == to_currency:
            return round(amount) if rounding else amount
        symbol = from_currency + to_currency
        price = get_price_or_none(SYMBOL=symbol)
        if price:
            converted_amount = price.ASK * amount
            return round(converted_amount) if rounding else converted_amount
        else:
            symbol = to_currency + from_currency
            price = get_price_or_none(SYMBOL=symbol)
            if price:
                converted_amount = (1 / price.ASK) * amount
                return round(converted_amount) if rounding else converted_amount
        # try double covert
        try:
            base_currency = Currency.objects.get(is_base=True)
        except Currency.DoesNotExist:
            return 0
        convert_to_base_amount = self.conv(amount, from_currency, base_currency.iso, rounding)
        if convert_to_base_amount:
            return self.conv(convert_to_base_amount, base_currency.iso, to_currency, rounding)
        return 0

