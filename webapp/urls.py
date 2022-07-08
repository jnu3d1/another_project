from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
