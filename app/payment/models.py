import json

from django.db import models


class PaymentSystem(models.Model):
    name = models.CharField(max_length=64, default=None)
    code = models.CharField(max_length=32, blank=False)
    cls = models.CharField(max_length=32, blank=False)
    is_enabled = models.BooleanField(blank=False, default=False)
    withdraw = models.BooleanField(blank=False, default=False)
    _config = models.TextField(
        db_column='config',
        verbose_name='config',
        name='config',
        blank=True,
        default=None
    )

    def _get_config(self):
        return json.loads(self._config)

    def _set_config(self, value):
        self._config = json.dumps(value)

    config = property(_get_config, _set_config)

    class Meta:
        db_table = "payment_systems"
