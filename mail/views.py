from django.shortcuts import render
from django.views.generic import ListView

from mail.models import Newsletter


class NewsletterListView(ListView):
    model = Newsletter
