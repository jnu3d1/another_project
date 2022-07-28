from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from webapp.forms import ProjectForm
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


class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = 'projects/create.html'

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.pk})


class EditProject(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'projects/edit.html'

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.pk})
