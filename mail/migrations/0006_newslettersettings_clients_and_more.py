# Generated by Django 4.2.5 on 2023-10-16 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('mail', '0005_rename_settings_newsletter_mail_settings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersettings',
            name='clients',
            field=models.ManyToManyField(to='client.client', verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='newslettersettings',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mail.newsletter', verbose_name='сообщение рассылки'),
        ),
    ]