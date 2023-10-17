from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail

from mail.models import Newsletter, NewsletterSettings


def send_massage(subject, message, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False
    )


def start_newsletter(newsletter: Newsletter, clients: list):
    if datetime.now().strftime('%y-%m-%d %H:%M:%S') >=\
            newsletter.mail_settings.finish_time.strftime('%y-%m-%d %H:%M:%S'):
        newsletter_settings = NewsletterSettings.objects.filter(newsletter=newsletter)
        newsletter_settings.status = 'ST'
    send_massage(newsletter.subject, newsletter.body, clients)
    if datetime.now().strftime('%y-%m-%d %H:%M:%S') >=\
            newsletter.mail_settings.finish_time.strftime('%y-%m-%d %H:%M:%S'):
        newsletter_settings = NewsletterSettings.objects.filter(newsletter=newsletter)
        newsletter_settings.status = 'FI'

