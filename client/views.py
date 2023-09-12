from django.shortcuts import render
from django.views.generic import ListView

from client.models import Client


class ClientListView(ListView):
    model = Client
