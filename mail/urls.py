from django.urls import path

from mail.views import NewsletterListView

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletter_list'),
]
