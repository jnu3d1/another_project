from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView

from webapp.forms import IssueForm
from webapp.models import Issue


class IndexView(ListView):
    model = Issue
    template_name = 'index.html'
    context_object_name = 'issues'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by('status', '-updated_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class IssueView(TemplateView):
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=pk)
        kwargs['issue'] = issue
        return super().get_context_data(**kwargs)


class CreateIssue(View):
    def get(self, request):
        form = IssueForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            types = form.cleaned_data.pop('types')
            new_issue = Issue.objects.create(summary=summary, description=description, status=status)
            new_issue.types.set(types)
            return redirect('issue', pk=new_issue.pk)
        return render(request, 'create.html', {'form': form})


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
            return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            self.issue.summary = form.cleaned_data.get('summary')
            self.issue.description = form.cleaned_data.get('description')
            self.issue.status = form.cleaned_data.get('status')
            self.issue.types.set(form.cleaned_data.pop('types'))
            self.issue.save()
            return redirect('issue', pk=self.issue.pk)
        return render(request, 'edit.html', {'form': form})


class DeleteIssue(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.issue = get_object_or_404(Issue, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return render(request, 'delete.html', {'issue': self.issue})

    def post(self, request, *args, **kwargs):
        self.issue.delete()
        return redirect('index')
