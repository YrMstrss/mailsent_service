from django.contrib import admin

from mail.models import Newsletter


@admin.register(Newsletter)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'body')
    search_fields = ('subject', 'body')

