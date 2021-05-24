from io import BytesIO
from .exceptions import UnknownFormatError

_delim = b':'
_formats = {}


def _bytes(seq):
    return seq.encode() if hasattr(seq, 'encode') else seq


def register(code, renderer, parser):
    code = _bytes(code)
    _formats[code] = {
        'renderer': renderer,
        'parser': parser,
    }


def unpack(data):
    pass


def unregister(code):
    code = _bytes(code)
    try:
        del _formats[code]
    except KeyError:
        pass


def render(code, data):
    code = _bytes(code)
    if code not in _formats:
        raise UnknownFormatError('Could not find renderer for format %s' % code.decode())
    body = _formats[code]['renderer'].render(data)
    return code + _delim + body


def parse(data):
    return _formats[b'json']['parser'].parse(BytesIO(_bytes(data)))


__all__ = ['register', 'unregister', 'render', 'parse']
