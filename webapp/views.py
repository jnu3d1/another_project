from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from webapp.models import Issue, Status, Type


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        issues = Issue.objects.order_by('-status')
        return render(request, 'index.html', {'issues': issues})
