from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView

from client.models import Client
from mail.models import Newsletter, NewsletterSettings


class home_page(TemplateView):
    template_name = 'mail/home.html'

    def get_context_data(self, **kwargs):
        context = {}
        newsletters = Newsletter.objects.all().count()
        clients = Client.objects.all().count()
        context['newsletters'] = newsletters
        context['clients'] = clients
        return context


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    fields = ('subject', 'body', 'settings')
    success_url = reverse_lazy('mail:newsletter_list')


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    fields = ('subject', 'body', 'settings')
    success_url = reverse_lazy('mail:newsletter_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mail:newsletter_list')
