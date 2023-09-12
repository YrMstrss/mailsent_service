from django.urls import path

from mail.apps import MailConfig
from mail.views import NewsletterListView, home_page, NewsletterCreateView, NewsletterDetailView

app_name = MailConfig.name

urlpatterns = [
    path('', home_page, name='home'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_view')
]
