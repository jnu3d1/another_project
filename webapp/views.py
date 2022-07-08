from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import IssueForm
from webapp.models import Issue, Status, Type


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        issues = Issue.objects.order_by('-status')
        return render(request, 'index.html', {'issues': issues})


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
            type = form.cleaned_data.get('type')
            new_issue = Issue.objects.create(summary=summary, description=description, status=status, type=type)
            return redirect('issue', pk=new_issue.pk)
        return render(request, 'create.html', {'form': form})
