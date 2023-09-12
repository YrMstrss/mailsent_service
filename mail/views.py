from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from mail.models import Newsletter


def home_page(request):
    return render(request, "mail/home.html")


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    fields = ('subject', 'body')
    success_url = reverse_lazy('mail:newsletter_list')
