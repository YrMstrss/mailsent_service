from django.urls import path

from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView

app_name = ClientConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit')
]