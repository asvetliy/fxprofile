class PammKafkaError(Exception):
    pass


class UnknownFormatError(PammKafkaError):
    pass


class IgnoredMessageTypeError(PammKafkaError):
    pass


class UnknownMessageTypeError(PammKafkaError):
    pass


class UnknownMessageVersionError(PammKafkaError):
    pass


class InvalidMessageError(PammKafkaError):
    pass


class MissingTopicError(PammKafkaError):
    pass
