from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('webapp.add_project'):
            return super().dispatch(request, *args, **kwargs)
        return redirect('accounts:login')

    def form_valid(self, form):
        author = self.request.user
        form.instance.author = author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'pk': self.object.pk})


class EditProject(LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'projects/edit.html'

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'pk': self.object.pk})


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('webapp:projects')
