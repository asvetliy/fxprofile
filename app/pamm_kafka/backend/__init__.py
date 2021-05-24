from collections import namedtuple
from django.utils.module_loading import import_string
from .. import settings


Record = namedtuple('Record', ['topic', 'partition', 'offset', 'timestamp', 'key', 'value'])


RecordMetadata = namedtuple('RecordMetadata', ['topic', 'partition', 'offset'])


def get_offset_backend():
    default = 'pamm_kafka.backend.kafka.ModelOffsetStore'
    backend_path = settings.get('OFFSET_BACKEND', default)
    return import_string(backend_path)()


def get_consumer_backend(topic_name, **kwargs):
    default = 'pamm_kafka.backend.kafka.Consumer'
    backend_path = settings.get('CONSUMER_BACKEND', default)
    return import_string(backend_path)(topic_name, **kwargs)
