from django.conf import settings
from django.db import models

from client.models import Client

NULLABLE = {'null': True, 'blank': True}


class NewsletterSettings(models.Model):

    STATUS_CHOICES = [
        ('CR', 'Создана'),
        ('ST', 'Запущена'),
        ('FI', 'Завершена'),

    ]

    PERIOD_CHOICES = [
        ('HR', 'Часовая'),
        ('DL', 'Ежедневная'),
        ('WK', 'Еженедельная')
    ]

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='CR', verbose_name='статус рассылки')
    start_time = models.DateTimeField(verbose_name='время начала рассылки', **NULLABLE)
    finish_time = models.DateTimeField(verbose_name='время окончания рассылки', **NULLABLE)
    period = models.CharField(max_length=2, choices=PERIOD_CHOICES, verbose_name='периодичность')

    def __str__(self):
        return f'{self.status}, {self.period} ({self.start_time} - {self.finish_time})'

    class Meta:

        permissions = [
            ('set_newsletter_status', 'Can change newsletter status')
        ]

        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'


class Newsletter(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема')
    body = models.TextField(verbose_name='содержание')

    mail_settings = models.ForeignKey(NewsletterSettings, on_delete=models.CASCADE, verbose_name='настройка рассылки')

    clients = models.ManyToManyField(Client, verbose_name='клиент')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='создатель')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
