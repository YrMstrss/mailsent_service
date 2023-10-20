from django.conf import settings
from django.db import models

from client.models import Client

NULLABLE = {'null': True, 'blank': True}


class NewsletterSettings(models.Model):

    """
    Модель настроек рассылки.
    Поля: 'status' - отвечает за статус рассылки. Определяется автоматически из 3ех значений приведенных в переменной
    'STATUS_CHOICES'
    'start_time' и 'finish_time' - время начала и окончания рассылки
    'period' - поле для выбора периодичности рассылки. Выбирается из значений 'PERIOD_CHOICES'
    """

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
    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    finish_time = models.DateTimeField(verbose_name='время окончания рассылки')
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

    """
    Модель рассылки
    Поля: 'subject' - тема отправляемого сообщения
    'body' - содержание отправляемого сообщения
    'mail_settings' - подключенные настройки рассылки
    'clients' - поле, отвечающее за клиентов, которым будет отправлено заданное сообщение
    'creator' - пользователь, создавший и управляющий данной рассылкой
    """

    subject = models.CharField(max_length=150, verbose_name='тема')
    body = models.TextField(verbose_name='содержание')

    mail_settings = models.ForeignKey(NewsletterSettings, on_delete=models.CASCADE, verbose_name='настройка рассылки')

    clients = models.ManyToManyField(Client, verbose_name='клиент')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='создатель')

    is_active = models.BooleanField(default=True, verbose_name='активность рассылки')

    job_id = models.CharField(default='', verbose_name='id задачи')

    def __str__(self):
        return f'{self.subject}'

    class Meta:

        permissions = [
            ('view_all', 'Can view all newsletters')
        ]
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class NewsletterLogs(models.Model):
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки')
    server_answer = models.TextField(verbose_name='ответ сервера')
    status = models.BooleanField(verbose_name='статус')

    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'{self.last_try}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
