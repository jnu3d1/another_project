from django.views.generic import ListView

from webapp.models import Project


class ProjectsView(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    ordering = ('start_date',)
