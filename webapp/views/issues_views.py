from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from webapp.forms import IssueForm, SearchForm
from webapp.models import Issue, Project


class IndexView(ListView):
    model = Issue
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Issue.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return super().get_queryset().order_by('status', '-updated_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')


class IssueView(TemplateView):
    template_name = 'issues/issue.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=pk)
        kwargs['issue'] = issue
        return super().get_context_data(**kwargs)


class CreateIssue(CreateView):
    form_class = IssueForm
    template_name = 'issues/create.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.project.pk})


class EditIssue(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.issue = get_object_or_404(Issue, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = IssueForm(initial={
                'summary': self.issue.summary,
                'description': self.issue.description,
                'status': self.issue.status,
                'types': self.issue.types.all()
            })
            return render(request, 'issues/edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            self.issue.summary = form.cleaned_data.get('summary')
            self.issue.description = form.cleaned_data.get('description')
            self.issue.status = form.cleaned_data.get('status')
            self.issue.types.set(form.cleaned_data.pop('types'))
            self.issue.save()
            return redirect('issue', pk=self.issue.pk)
        return render(request, 'issues/edit.html', {'form': form})


class DeleteIssue(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.issue = get_object_or_404(Issue, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return render(request, 'issues/delete.html', {'issue': self.issue})

    def post(self, request, *args, **kwargs):
        self.issue.delete()
        return redirect('projects')
