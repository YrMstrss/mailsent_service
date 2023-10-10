import secrets

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileChangeForm
# Create your views here.
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_urlsafe(nbytes=8)

        user.token = token
        activate_url = reverse_lazy('users:email_verified', kwargs={'token': user.token})
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: '
                    f'http://localhost:8000/{activate_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        user.save()

        return redirect('users:email_sent')


class UserConfirmEmailView(View):
    def get(self, request, token):
        user = User.objects.get(token=token)

        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmailConfirmView(TemplateView):
    template_name = 'users/verified.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileChangeForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        return self.request.user
