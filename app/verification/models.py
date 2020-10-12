from django.db import models
from django.conf import settings
from .validators import validate_file
from os.path import splitext
from django.utils.crypto import get_random_string


def user_directory_path(instance, old_file_name):
    filename = get_random_string(length=32)
    name, extension = splitext(old_file_name)
    return f'docs/{instance.user.id}/{filename}{extension}'


class RequestType(models.Model):
    enabled = models.BooleanField(default=False, blank=False, null=False)
    required = models.BooleanField(default=True, blank=False, null=False)
    name = models.CharField(max_length=32, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True, null=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'request_type'


class CardsType(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True, null=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'card_type'


class RequestStatus(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'request_status'


class Card(models.Model):
    number = models.CharField(max_length=16, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    type = models.ForeignKey(CardsType, models.DO_NOTHING, null=True, blank=False, default=None)
    is_verificated = models.BooleanField(null=False, default=False, blank=False)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'cards'


class VerificationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    old_file_name = models.CharField(max_length=128, blank=False, null=False)
    file = models.FileField(
        upload_to=user_directory_path,
        default=None,
        blank=True,
        null=True,
        validators=[validate_file],
    )
    type = models.ForeignKey(RequestType, models.DO_NOTHING)
    status = models.ForeignKey(RequestStatus, models.DO_NOTHING)
    card = models.ForeignKey(Card, models.CASCADE, blank=True, null=True, default=None)
    comment = models.CharField(max_length=256, blank=True, null=False, default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'verification_requests'


class Verification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    declaration = models.ForeignKey(VerificationRequest, models.DO_NOTHING, null=True, default=None, blank=False, related_name='declaration_set')
    identification = models.ForeignKey(VerificationRequest, models.DO_NOTHING, null=True, default=None, blank=False, related_name='identification_set')
    invoice = models.ForeignKey(VerificationRequest, models.DO_NOTHING, null=True, default=None, blank=False, related_name='invoice_set')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'verifications'
