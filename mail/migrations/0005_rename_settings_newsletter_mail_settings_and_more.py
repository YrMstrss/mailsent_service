# Generated by Django 4.2.5 on 2023-10-14 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0004_newsletter_clients'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='settings',
            new_name='mail_settings',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='создатель'),
        ),
    ]
