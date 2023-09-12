from django.db import models


class Newsletter(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема')
    body = models.TextField(verbose_name='содержание')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
