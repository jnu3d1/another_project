from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView

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
