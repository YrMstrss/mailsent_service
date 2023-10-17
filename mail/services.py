import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore

from client.models import Client
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


logger = logging.getLogger(__name__)

scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


def run_scheduler(newsletter: Newsletter):

    clients = Client.objects.filter(newsletter=newsletter)
    clients_email = [client.email for client in clients]

    if newsletter.mail_settings.start_time:
        start_time = newsletter.mail_settings.start_time
    else:
        start_time = datetime.now()

    if newsletter.mail_settings.finish_time:
        finish_time = newsletter.mail_settings.finish_time
    else:
        finish_time = start_time + timedelta(days=365)

    if newsletter.mail_settings.period == 'HR':
        trigger = CronTrigger(second=start_time.second)
        # trigger = CronTrigger(second=start_time.second,
        #                       minute=start_time.minute,
        #                       start_date=start_time, end_date=finish_time)
    elif newsletter.mail_settings.period == 'DL':
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              start_date=start_time, end_date=finish_time)
    else:
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              day_of_week=start_time.weekday(),
                              start_date=start_time, end_date=finish_time)

    scheduler.add_job(
        start_newsletter,
        kwargs={'newsletter': newsletter, 'clients': clients_email},
        trigger=trigger,
        id=f"start_newsletter {newsletter} ({newsletter.pk})",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info(f"Added job '{id}'.")
