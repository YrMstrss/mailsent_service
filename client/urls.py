from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('clients/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
]