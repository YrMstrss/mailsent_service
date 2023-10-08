import logging
from datetime import datetime, timedelta

from mail.models import Newsletter
from mail.services import start_newsletter, get_newsletter_list

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            get_newsletter_list,
            trigger=CronTrigger(second='0'),
            id="get_newsletter_list",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info(f"Added job '{id}'.")

        for letter in get_newsletter_list():

            clients = list(letter.clients.all())

            if letter.settings.start_time:
                start_time = letter.settings.start_time
            else:
                start_time = datetime.now()

            if letter.settings.finish_time:
                finish_time = letter.settings.finish_time
            else:
                finish_time = start_time + timedelta(days=365)

            if letter.settings.period == 'HR':
                trigger = CronTrigger(second=start_time.second,
                                      minute=start_time.minute,
                                      start_date=start_time, end_date=finish_time)
            elif letter.settings.period == 'DL':
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
                kwargs={'newsletter': letter, 'clients': clients},
                trigger=trigger,
                id=f"start_newsletter {letter}",  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
            logger.info(f"Added job '{id}'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
