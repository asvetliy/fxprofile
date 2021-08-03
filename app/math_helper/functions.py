def int_to_amount(amount: int, digest: int = 2) -> str:
    return '%.*f' % (digest, amount / pow(10, digest))


def amount_to_int(amount: str, digest: int = 2) -> str:
    return '%u' % (int(float(amount) * pow(10, digest)))


def ftoi(f: float, d: int = 2) -> int:
    """
    Converting float amount to integer

    :param f: float amount
    :param d: digits count
    :return: integer amount
    """
    return int(f * pow(10, d))


def itof(i: int, d: int = 2) -> float:
    """
    Converting integer amount to float amount

    :param i: integer amount
    :param d: digits count
    :return: float amount
    """
    return i * pow(10, -d)


def iper(a: int, b: int) -> int:
    if b == 0:
        return 0
    return round(a * 10000 / b)


def ishare(a: int, b: int) -> int:
    return int((a * b) / 10000)


def ishare_c(a: int, b: int) -> int:
    return int((a * (10000 - b)) / 10000)


def ftos(f: float, d: int = 2) -> str:
    return f'{f:.{d}f}'


def itos(i: int, d: int = 2) -> str:
    return ftos(itof(i, d), d)


def is_number(s: str) -> bool:
    """
    Returns True if string is a number

    :param s: integer amount
    :return: bool
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def ftime(t: str) -> str:
    if not t or t == '1970-01-01 00:00:00':
        return '-'
    return t
