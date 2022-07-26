from django.views.generic import ListView, DetailView

from webapp.models import Project


class ProjectsView(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    ordering = ('start_date',)


class ProjectView(DetailView):
    model = Project
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.order_by('status', '-updated_at')
        return context