from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Verification, Card, VerificationRequest

UserModel = get_user_model()


def is_user_verificated(user):
    cards = Card.objects.filter(user=user)
    for c in cards:
        if not c.is_verified:
            return False
    v = Verification.objects.get(user=user)
    if len(cards) and not v.declaration:
        return False
    if not v.identification or not v.invoice:
        return False
    return True


def is_card_verificated(card: Card):
    v = Verification.objects.get(user=card.user)
    if not v.declaration:
        return False

    if card.type_id == 1:
        verification_requests = VerificationRequest.objects.filter(user=card.user, card=card, type__in=(1, 2, ), status=1)
        if not len(verification_requests):
            return False

        front, back = False, False
        for vr in verification_requests:
            if vr.type_id == 1:
                front = True
            if vr.type_id == 2:
                back = True

        if not front or not back:
            return False

    if card.type_id == 2:
        verification_requests = VerificationRequest.objects.filter(user=card.user, card=card, type_id=1, status=1)
        if not len(verification_requests):
            return False

        front = False
        for vr in verification_requests:
            if vr.type_id == 1:
                front = True

        if not front:
            return False

    return True


def check_verification_status(instance: VerificationRequest):
    is_verified = is_user_verificated(instance.user)
    if is_verified != instance.user.is_verified:
        instance.user.is_verified = is_verified
        instance.user.save()


def check_card_verification_status(instance: VerificationRequest):
    if instance.card:
        is_verified = is_card_verificated(instance.card)
        if is_verified != instance.card.is_verified:
            instance.card.is_verified = is_verified
            instance.card.save()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        Verification.objects.create(user=instance)


@receiver(post_save, sender=VerificationRequest)
def request_saved(sender, instance, created, **kwargs):
    if not created and instance.status_id == 1:
        v = Verification.objects.get(user=instance.user)
        if instance.type_id in (1, 2, 3):
            check_card_verification_status(instance)
        if instance.type_id == 3:
            v.declaration = instance
            v.save()
        if instance.type_id == 4:
            v.identification = instance
            v.save()
        if instance.type_id == 5:
            v.invoice = instance
            v.save()
        check_verification_status(instance)
    elif not created:
        v = Verification.objects.get(user=instance.user)
        if instance.type_id in (1, 2, 3):
            check_card_verification_status(instance)
        if instance.type_id == 3:
            v.declaration = None
            v.save()
        if instance.type_id == 4:
            v.identification = None
            v.save()
        if instance.type_id == 5:
            v.invoice = None
            v.save()
        check_verification_status(instance)


@receiver(post_save, sender=Card)
def card_saved(sender, instance, created, **kwargs):
    if created:
        v = Verification.objects.get(user=instance.user)
        v.declaration = None
        v.save()
        check_verification_status(instance)
