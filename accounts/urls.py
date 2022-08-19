from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='create'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('change/', ProfileChangesView.as_view(), name='change'),
    path('change/password/', PasswordChangeView.as_view(), name='change_password'),
]
