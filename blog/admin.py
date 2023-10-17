from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'view_counter', 'created_at')
    search_fields = ('title', 'body')
