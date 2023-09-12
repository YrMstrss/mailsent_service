from django.shortcuts import render
from django.views.generic import ListView

from mail.models import Newsletter


def home_page(request):
    return render(request, "mail/home.html")


class NewsletterListView(ListView):
    model = Newsletter
