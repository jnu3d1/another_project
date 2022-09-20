import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from webapp.models import Project


# Create your views here.
def echo_view(request):
    answer = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': request.method,
    }
    if request.body:
        answer['content'] = json.loads(request.body)
    # answer_as_json = json.dumps(answer)
    # response = HttpResponse(answer_as_json)
    # response['Content-Type'] = 'application/json'
    response = JsonResponse(answer)
    return response


def projects_view(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        projects_fields = []
        for project in projects:
            projects_fields.append({
                'name': project.name,
                'description': project.description,
            })
        return JsonResponse(projects_fields, safe=False)
    elif request.method == 'POST':
        body = json.loads(request.body)
        project = Project.objects.create(**body)
        return JsonResponse({'id': project.pk})
    else:
        return HttpResponseNotAllowed('GET', 'POST')


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')
