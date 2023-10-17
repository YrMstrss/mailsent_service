from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):

    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    picture = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    view_counter = models.IntegerField(default=0, verbose_name='количество просмотров')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:

        verbose_name = 'статья блога'
        verbose_name_plural = 'статьи блога'
