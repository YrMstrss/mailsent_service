from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.EmailField(verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    clients = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='клиент', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.last_name} {self.first_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
