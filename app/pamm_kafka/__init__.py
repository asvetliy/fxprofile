from .formats.json import JSONRenderer, JSONParser
from .consumer import Consumer, MultiConsumer
from .registry import register_consumer
from . import format, settings


default_app_config = 'pamm_kafka.apps.PammKafkaConfig'
_default_format = settings.get('DEFAULT_FORMAT', 'json')
format.register('json', JSONRenderer(), JSONParser())


__all__ = [
    'Consumer',
    'MultiConsumer',
    'register_consumer',
]
