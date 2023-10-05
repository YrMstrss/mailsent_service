from django.conf import settings
from django.core.mail import send_mail


def send_massage(subject, message, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipients],
        fail_silently=False
    )
