from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    country = models.CharField(_('COUNTRY'), max_length=64, blank=False, null=True)
    city = models.CharField(_('CITY'), max_length=64, blank=False, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False, blank=False)
    about_me = models.TextField(max_length=1024, null=True, blank=True)
    phone = models.CharField(max_length=17, blank=True, default=None, null=True)
    promo = models.CharField(max_length=64, blank=True, default=None, null=True)
    is_verified = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class PartnerUser(User):

    class Meta:
        proxy = True
