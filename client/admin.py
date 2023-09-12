from django.contrib import admin

from client.models import Client


@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')

