from django.urls import path

from api_2.views import *

app_name = 'api_2'

urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('projects/<int:pk>/', ProjectsView.as_view()),
]