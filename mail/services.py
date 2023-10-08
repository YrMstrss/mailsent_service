from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail

from mail.models import Newsletter


def send_massage(subject, message, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False
    )


def start_newsletter(newsletter: Newsletter, clients: list):
    if datetime.now() >= newsletter.settings.finish_time:
        newsletter.settings.status = 'ST'
    send_massage(newsletter.subject, newsletter.body, clients)
    if datetime.now() >= newsletter.settings.finish_time:
        newsletter.settings.status = 'FI'


def get_newsletter_list():
    letters = list(Newsletter.objects.all())
    return letters
