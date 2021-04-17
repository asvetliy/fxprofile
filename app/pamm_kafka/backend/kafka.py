import kafka

from django.apps import apps
from ..exceptions import MissingTopicError
from .. import settings
from . import Record, get_offset_backend
from json_logging import log


class ModelOffsetStore(object):
    def commit(self, consumer, message):
        KafkaOffset = apps.get_model(app_label='pamm_kafka', model_name='KafkaOffset')
        log.debug('Commit offset "%s" for topic "%s", partition "%s" to %s' % (
            message.offset, message.topic, message.partition, self.__class__.__name__))
        obj, created = KafkaOffset.objects.get_or_create(
            topic=message.topic,
            partition=message.partition)
        obj.offset = message.offset + 1
        obj.save()

    def seek(self, consumer, topic, partition):
        KafkaOffset = apps.get_model(app_label='pamm_kafka', model_name='KafkaOffset')
        tp = kafka.TopicPartition(topic=topic, partition=partition)
        try:
            obj = KafkaOffset.objects.get(topic=topic, partition=partition)
            log.debug('Seeking to offset "%s" on topic "%s", partition "%s"' % (obj.offset, topic, partition))
            consumer.client.seek(tp, obj.offset)
        except KafkaOffset.DoesNotExist:
            log.debug('Seeking to beginning of topic "%s", partition "%s"' % (topic, partition))
            consumer.client.seek_to_beginning(tp)


class KafkaOffsetStore(object):
    def commit(self, consumer, message):
        log.debug('Commit offset "%s" for topic "%s", partition "%s" to %s' % (
            message.offset, message.topic, message.partition, self.__class__.__name__))
        consumer.client.commit()

    def seek(self, consumer, topic, partition):
        pass


class Consumer(object):
    _client = None

    def __init__(self, topic_name, **kwargs):
        self.topic_name = topic_name
        self.client_kwargs = kwargs

    @property
    def client(self):
        if not self._client:
            kwargs = self._get_client_config()
            self._client = kafka.KafkaConsumer(**kwargs)
            tps = self._get_topic_partitions()
            self._client.assign(tps)
            backend = get_offset_backend()
            for tp in tps:
                backend.seek(self, tp.topic, tp.partition)
                self._client.committed(tp)
        return self._client

    def __iter__(self):
        return self

    def __next__(self):
        r = next(self.client)
        record = Record(
            topic=r.topic,
            partition=r.partition,
            offset=r.offset,
            timestamp=r.timestamp,
            key=r.key,
            value=r.value)
        return record

    def _get_topic_partitions(self):
        p = []
        partitions = self.client.partitions_for_topic(self.topic_name)
        if not partitions:
            raise MissingTopicError(f'Could not find topic {self.topic_name}. Does it exist?')
        for partition in partitions:
            tp = kafka.TopicPartition(self.topic_name, partition=partition)
            p.append(tp)
        return p

    def _get_client_config(self):
        kwargs = {
            'auto_offset_reset': 'earliest',
            'enable_auto_commit': False,
            'consumer_timeout_ms': 1000,
        }
        kwargs.update(settings.get('KAFKA_CONSUMER_KWARGS', {}))
        kwargs.update(self.client_kwargs)
        kwargs.update({
            'bootstrap_servers': settings.get('KAFKA_BOOTSTRAP_SERVERS'),
        })
        return kwargs
