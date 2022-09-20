import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from api_2.serializers import ProjectSerializer
from webapp.models import Project


# Create your views here.
class ProjectsView(View):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        projects_fields = ProjectSerializer(projects, many=True).data
        return JsonResponse(projects_fields, safe=False)

    def post(self, request, *args, **kwargs):
        if request.body:
            data = json.loads(request.body)
            serializer = ProjectSerializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                # Project.objects.create(**serializer.validated_data)
                serializer.save()
                return JsonResponse(serializer.data)
            except ValidationError as error:
                return JsonResponse({'error': serializer.errors}, status=400)
        return JsonResponse({'message': 'Error'}, status=400)

    def put(self, request, *args, pk, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if request.body:
            data = json.loads(request.body)
            serializer = ProjectSerializer(data=data, instance=project)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data)
            except ValidationError as error:
                return JsonResponse({'error': serializer.errors}, status=400)
        return JsonResponse({'message': 'Error'}, status=400)
