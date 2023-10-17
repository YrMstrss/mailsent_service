import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView

from blog.models import Blog
from client.models import Client
from mail.forms import NewsletterForm, NewsletterSettingsForm
from mail.models import Newsletter, NewsletterSettings
from mail.services import run_scheduler


class home_page(TemplateView):
    """
    Контроллер домашней страницы
    """
    template_name = 'mail/home.html'

    def get_context_data(self, **kwargs):
        """
        Метод получающий контекстную информацию, выводимую на домашней странице (общее количество рассылок, число
        активных рассылок, число клиентов и 3 случайные статьи блога)
        """
        context = {}
        newsletters = Newsletter.objects.all().count()

        active_newsletters = 0
        for newsletter in Newsletter.objects.all():
            if newsletter.mail_settings.status == 'ST':
                active_newsletters += 1

        clients = Client.objects.all().count()

        if Blog.objects.all().count() > 3:
            blog_numbers = [random.randint(0, Blog.objects.all().count() - 1) for _ in range(3)]
            for i in range(3):
                context[f'blog{i}'] = Blog.objects.all()[blog_numbers[i]]
        else:
            for i in range(Blog.objects.all().count()):
                context[f'blog{i}'] = Blog.objects.all()[i]

        context['newsletters'] = newsletters
        context['active_newsletters'] = active_newsletters
        context['clients'] = clients
        if self.request.user.has_perm('users.view_user_list_user'):
            context['users'] = 'Пользователи'
        return context


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('mail.view_all_newsletter'):
            context['object_list'] = Newsletter.objects.all()
        else:
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

        run_scheduler(self.object)

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
