import itertools
import time

from django.db import transaction
from rest_framework.exceptions import ValidationError
from .exceptions import InvalidMessageError, IgnoredMessageTypeError, UnknownMessageTypeError, UnknownMessageVersionError
from .backend import get_offset_backend, get_consumer_backend
from .format import parse
from . import settings
from json_logging import log


def consumer_error_handler(inner):
    while True:
        # Try to get the next message
        try:
            yield next(inner)

        # Obey the laws of StopIteration
        except StopIteration:
            return

        # Message format was invalid in some way: log error and move on.
        except InvalidMessageError as e:
            log.error(f'Failed to deserialize message in topic {inner.consumer.topic_name}. Details: {e}')
            inner.commit(e.message)

        # Message type has been explicitly ignored: skip it silently and move on.
        except IgnoredMessageTypeError as e:
            log.debug(f'Skipping ignored message type in topic {inner.consumer.topic_name}. Details: {e}')
            inner.commit(e.message)

        # Message type is unknown: log error and move on.
        except UnknownMessageTypeError as e:
            log.error(f'Skipping unknown message type in topic {inner.consumer.topic_name}. Details: {e}')
            inner.commit(e.message)

        # Message version is unknown: log error and move on.
        except UnknownMessageVersionError as e:
            log.error(f'Skipping unknown message version in topic {inner.consumer.topic_name}. Details: {e}')
            inner.commit(e.message)

        # Serializer for message type flagged message as invalid: log warning and move on.
        except ValidationError as e:
            log.warning(f'Skipping invalid message in topic {inner.consumer.topic_name}. Details: {e}')
            inner.commit(e.message)

        pass


class Consumer(object):
    _client = None

    def __init__(self, topic_name, throw_errors=False, **kwargs):
        self.consumer = get_consumer_backend(topic_name, **kwargs)
        self.throw_errors = throw_errors
        self.serializer_classes = {}
        self.ignored_message_types = set([])

    def add_ignored_message_type(self, message_type):
        self.ignored_message_types.add(message_type)

    def commit(self, message):
        get_offset_backend().commit(self.consumer, message)

    def register(self, serializer_class):
        message_type = serializer_class.MESSAGE_TYPE
        if message_type not in self.serializer_classes:
            self.serializer_classes[message_type] = {}
        self.serializer_classes[message_type] = serializer_class

    def run(self, iter_limit=0):
        i = 0
        for message, serializer in self:
            with transaction.atomic():
                try:
                    serializer.save()
                    self.commit(message)
                except Exception as e:
                    info = (message.key, message.topic, message.partition, message.offset)
                    log.exception('Failed to process message with key "%s" from topic "%s", partition "%s", offset "%s"' % info)
                    raise e
            i += 1
            if 0 < iter_limit <= i:
                break

    def __iter__(self):
        if self.throw_errors:
            return self
        return consumer_error_handler(self)

    def __next__(self):
        return self._get_next_message()

    def __str__(self):
        return '<pamm_kafka.consumer.Consumer topic="%s">' % self.consumer.topic_name

    def _get_next_message(self):
        message = next(self.consumer)

        info = (message.key, message.topic, message.partition, message.offset)
        log.debug('Received message with key "%s" from topic "%s", partition "%s", offset "%s"' % info)

        # Wait?
        timestamp = getattr(message, 'timestamp', None) or (time.time() * 1000)
        lag_ms = (time.time() * 1000) - timestamp
        log.debug("Message lag is %sms" % lag_ms)
        wait_ms = settings.get('MIN_MESSAGE_LAG_MS', 0) - lag_ms
        if wait_ms > 0:
            log.debug("Respecting MIN_MESSAGE_LAG_MS by waiting %sms" % wait_ms)
            time.sleep(wait_ms / 1000)
            log.debug("Finished waiting")

        try:
            serializer = self._unserialize(message)
        except Exception as e:
            e.message = message
            raise e

        return message, serializer

    def _unserialize(self, message):
        data = parse(message.value)
        if 'type' not in data:
            raise InvalidMessageError

        message_type = data['type']
        if message_type in self.ignored_message_types:
            raise IgnoredMessageTypeError
        if message_type not in self.serializer_classes:
            raise UnknownMessageTypeError

        serializer_class = self.serializer_classes[message_type]

        instance = None
        if hasattr(serializer_class, 'lookup_instance'):
            instance = serializer_class.lookup_instance(**data)
        serializer = serializer_class(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        return serializer


class MultiConsumer(object):
    def __init__(self, *consumers):
        self.consumers = consumers

    def run(self):
        for consumer in itertools.cycle(self.consumers):
            consumer.run(iter_limit=1)
