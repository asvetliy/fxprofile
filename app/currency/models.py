from django.db import models


class Currency(models.Model):
    iso = models.CharField(max_length=4, blank=False)
    symbol = models.CharField(max_length=4, blank=False)
    name = models.CharField(max_length=32, blank=True)
    digest = models.IntegerField(default=2, blank=False)
    is_default = models.BooleanField(default=False, blank=False)
    is_base = models.BooleanField(default=False, blank=False)
    is_enabled = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.iso

    def get_base(self):
        return self.objects.get(is_base=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_base:
            self.objects.filter(is_base=True).update(is_base=False)
        super(Currency, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'currencies'
        verbose_name_plural = 'currencies'
