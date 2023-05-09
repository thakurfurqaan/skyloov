from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

from registration.tasks import send_welcome_email
from skyloov.settings import WELCOME_EMAIL_DELAY_SECONDS


@receiver(post_save, sender=User)
def send_welcome_email_if_new(sender, instance, created, **kwargs):
    if (
        created
        and (timezone.now() - instance.date_joined).total_seconds()
        < WELCOME_EMAIL_DELAY_SECONDS
    ):
        print(
            f"New registration email will be sent to {instance.email} after {WELCOME_EMAIL_DELAY_SECONDS} seconds."
        )
        send_welcome_email.apply_async(
            args=[instance.id], countdown=WELCOME_EMAIL_DELAY_SECONDS
        )
