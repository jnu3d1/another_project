from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProjectForm, ProjectUsersForm
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
        if request.user.is_authenticated:
            if request.user.has_perm('webapp.add_project'):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return redirect('accounts:login')

    def form_valid(self, form):
        author = self.request.user
        form.instance.author = author
        # response = super().form_valid(form)
        # self.object.users.add(author)
        # return response
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'pk': self.object.pk})


class EditProject(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    model = Project
    permission_required = 'webapp.change_project'
    template_name = 'projects/edit.html'

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'pk': self.object.pk})


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'webapp.delete_project'
    success_url = reverse_lazy('webapp:projects')
    template_name = 'projects/delete.html'


class ProjectUsersView(PermissionRequiredMixin, UpdateView):
    form_class = ProjectUsersForm
    model = Project
    permission_required = 'webapp.custom_permission'
    template_name = 'projects/project_users.html'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.users.all()

    def get_success_url(self):
        return reverse('webapp:project', kwargs={'pk': self.object.pk})


class AllUsersView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'projects/users.html'
    context_object_name = 'users'
    permission_required = 'webapp.custom_permission'