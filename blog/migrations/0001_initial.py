# Generated by Django 4.2.5 on 2023-10-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('body', models.TextField(verbose_name='содержимое')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='изображение')),
                ('view_counter', models.IntegerField(verbose_name='количество просмотров')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='дата публикации')),
            ],
            options={
                'verbose_name': 'статья блога',
                'verbose_name_plural': 'статьи блога',
            },
        ),
    ]