from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

from skyloov.settings import EMAIL_HOST_USER


@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)
    print(f"New registration email is being sent to {user.email}...")
    subject = "Welcome to Skyloov!"
    message = f"Hi {user.username}, thank you for joining our platform! Explore Over 48,000 properties around the emirates with https://skyloov.com/."
    send_mail(subject, message, EMAIL_HOST_USER, [user.email])
