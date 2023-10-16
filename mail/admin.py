from django.contrib import admin

from mail.models import Newsletter, NewsletterSettings


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'body', 'mail_settings', 'creator')
    search_fields = ('subject', 'body')


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'start_time', 'finish_time', 'period')

