from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmView, \
    Login, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', Login.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='user_list'),

    path('email-sent/', EmailConfirmationSentView.as_view(), name='email_sent'),
    path('confirm-email/<str:token>/', UserConfirmEmailView.as_view(), name='email_verified'),
    path('email_verified/', EmailConfirmView.as_view(), name='email_verified'),
]
