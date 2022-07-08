from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue'),
    path('issues/add/', CreateIssue.as_view(), name='create'),
    path('issue/<int:pk>/editing/', EditIssue.as_view(), name='edit'),
]
