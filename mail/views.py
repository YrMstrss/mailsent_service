from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView

from client.models import Client
from mail.forms import NewsletterForm, NewsletterSettingsForm
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


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Newsletter.objects.filter(creator=self.request.user)
        return context


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(newsletter=self.object)
        return context


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mail:newsletter_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mail:newsletter_list')


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mail:newsletter_list')


class NewsletterSettingsCreateView(LoginRequiredMixin, CreateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('mail:newsletter_list')
