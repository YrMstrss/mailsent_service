from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from client.models import Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment')
    success_url = reverse_lazy('client:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment')
    success_url = reverse_lazy('client:client_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client
