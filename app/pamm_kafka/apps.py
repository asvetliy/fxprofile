from django.apps import AppConfig
from logpipe import Consumer, register_consumer
from .serializers import KafkaSerializer


class PammKafkaConfig(AppConfig):
    name = 'pamm_kafka'


@register_consumer
def build_person_consumer():
    consumer = Consumer('pamm')
    consumer.register(KafkaSerializer)
    return consumer
