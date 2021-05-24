from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from .registry import register_consumer
from .consumer import Consumer
from .pamm_serializers import MessageSerializer, EventSerializer


class PammKafkaConfig(AppConfig):
    name = 'pamm_kafka'
    label = 'pamm_kafka'
    verbose_name = _('PammKafka')


# Register consumers with logpipe
@register_consumer
def build_person_consumer():
    consumer = Consumer('pamm')
    consumer.add_ignored_message_type('MESSAGE')
    consumer.register(MessageSerializer)
    consumer.register(EventSerializer)
    return consumer
