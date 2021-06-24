class PaymentStatus(object):
    DONE = 1
    PROCESS = 2
    FAIL = 3
    EXPIRE = 4
    ERROR = 5
    DECLINE = 6


ROCKSPAY_CURRENCIES = {
    'RUB': 1,
    'USD': 2,
    'EUR': 4,
}
