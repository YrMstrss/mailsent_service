from django.urls import path
from django.views.decorators.cache import cache_page

from mail.apps import MailConfig
from mail.views import NewsletterListView, NewsletterCreateView, NewsletterDetailView, NewsletterDeleteView, \
    NewsletterUpdateView, home_page, NewsletterSettingsCreateView, NewsletterLogsListView, toggle_newsletter_activity

app_name = MailConfig.name

urlpatterns = [
    path('', cache_page(60)(home_page.as_view()), name='home'),
    path('newsletters/', cache_page(60)(NewsletterListView.as_view()), name='newsletter_list'),
    path('newsletters/create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_view'),
    path('newsletters/delete/<int:pk>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletters/edit/<int:pk>', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/settings/create/', NewsletterSettingsCreateView.as_view(), name='newsletter_settings_create'),
    path('newsletters/logs/<int:pk>', NewsletterLogsListView.as_view(), name='newsletter_logs_list'),
    path('activity/<int:pk>', toggle_newsletter_activity, name='toggle_newsletter_activity'),
]
