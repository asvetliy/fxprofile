from django.db import models
from django.utils.translation import gettext_lazy as _


class KafkaOffset(models.Model):
    # Translators: Internal Model Field Name
    topic = models.CharField(
        _('Kafka Topic Name'),
        # Translators: Interal Model Field Help Text
        help_text=_('The Kafka topic name'),
        max_length=200
    )

    # Translators: Internal Model Field Name
    partition = models.PositiveIntegerField(
        _('Kafka Partition ID'),
        # Translators: Interal Model Field Help Text
        help_text=_('The Kafka partition identifier')
    )

    # Translators: Internal Model Field Name
    offset = models.PositiveIntegerField(
        _('Kafka Offset'),
        # Translators: Interal Model Field Help Text
        help_text=_('The current offset in the Kafka partition'),
        default=0
    )

    class Meta:
        # Translators: Internal Model Name (singular)
        verbose_name = _('Kafka Offset')
        # Translators: Internal Model Name (plural)
        verbose_name_plural = _('Kafka Offsets')
        unique_together = ('topic', 'partition')
        ordering = ('topic', 'partition', 'offset')

    def __str__(self):
        return 'topic="{}", partition="{}", offset="{}"'.format(self.topic, self.partition, self.offset)
