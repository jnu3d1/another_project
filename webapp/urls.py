from django.urls import path

from webapp.views import *

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue'),
    path('/project/<int:pk>/issues/add/', CreateIssue.as_view(), name='create'),
    path('issue/<int:pk>/editing/', EditIssue.as_view(), name='edit'),
    path('issue/<int:pk>/delete/', DeleteIssue.as_view(), name='delete'),
    path('', ProjectsView.as_view(), name='projects'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project'),
    path('projects/add/', CreateProject.as_view(), name='create_project'),
    path('project/<int:pk>/editing/', EditProject.as_view(), name='edit_project'),
]
