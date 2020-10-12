def int_to_amount(amount, digest):
    return '%.*f' % (digest, amount / 100)


def amount_to_int(amount, digest):
    return


def ftoi(f: float, d: int = 2) -> int:
    return int(f * pow(10, d))


def itof(i: int, d: int = 2) -> float:
    return i * pow(10, -d)


def iper(a: int, b: int) -> int:
    if b == 0:
        return 0
    return round(a * 10000 / b)


def ishare(a: int, b: int) -> int:
    return int((a * b) / 10000)


def ishare_c(a: int, b: int) -> int:
    return int((a * (10000 - b)) / 10000)


def ftos(f: float, d: int = 2):
    return f'{f:.{d}f}'


def itos(i: int, d: int = 2):
    return ftos(itof(i, d), d)


def ftime(t: str):
    if not t or t == '1970-01-01 00:00:00':
        return '-'
    return t
