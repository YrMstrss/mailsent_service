# Generated by Django 4.2.5 on 2023-10-16 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('deactivate_user', 'Can block or unblock users')], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
