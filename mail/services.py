from smtplib import SMTPException

from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from client.models import Client
from mail.models import Newsletter, NewsletterLogs


def send_massage(newsletter: Newsletter):
    """
    Функция для отправки сообщения и создания логов
    """
    clients = Client.objects.filter(newsletter=newsletter)

    for client in clients:

        try:
            send_mail(
                subject=newsletter.subject,
                message=newsletter.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )

            log = NewsletterLogs.objects.create(server_answer='200', status='успешно отправлена',
                                                newsletter=newsletter)
            log.save()
        except SMTPException as error:
            log = NewsletterLogs.objects.create(server_answer=error.args, status='ошибка отправки',
                                                newsletter=newsletter)
            log.save()


def create_task(scheduler, newsletter: Newsletter):
    """
    Функция, создающая новую задачу
    """
    newsletter.job_id = f'start_newsletter {newsletter} ({newsletter.pk})'
    newsletter.save()

    start_time = newsletter.mail_settings.start_time
    finish_time = newsletter.mail_settings.finish_time

    if newsletter.mail_settings.period == 'HR':
        trigger = CronTrigger(minute='*')
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
        send_massage,
        kwargs={'newsletter': newsletter},
        trigger=trigger,
        id=newsletter.job_id,
        max_instances=1,
        replace_existing=True,
    )


def check_time(newsletter: Newsletter) -> bool:
    if now() <= newsletter.mail_settings.finish_time:
        if now() >= newsletter.mail_settings.start_time:
            newsletter.mail_settings.status = 'ST'
            newsletter.mail_settings.save()

            log = NewsletterLogs.objects.create(server_answer='-', status='запущена', newsletter=newsletter)
            log.save()
            return True
        else:
            return False
    else:
        newsletter.mail_settings.status = 'FI'
        newsletter.mail_settings.save()

        log = NewsletterLogs.objects.create(server_answer='-', status='завершена', newsletter=newsletter)
        log.save()
        return False


def start_scheduler(scheduler):
    newsletters = Newsletter.objects.filter(is_active=True)

    if newsletters:
        for newsletter in newsletters:
            if newsletter.mail_settings.status != 'FI':
                job_id = f"start_newsletter {newsletter} ({newsletter.pk})"
                if check_time(newsletter):
                    if not scheduler.get_job(job_id):
                        create_task(scheduler, newsletter)
                else:
                    if scheduler.get_job(job_id):
                        scheduler.pause_job(job_id)

        if scheduler.state == 0:
            scheduler.start()
