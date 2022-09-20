import json

from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from django.views import View
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from api_2.serializers import ProjectSerializer, ProjectModelSerializer
from webapp.models import Project


# Create your views here.


class ProjectsView(APIView):
    serializer_class = ProjectModelSerializer

    def get(self, request, *args, **kwargs):
        if self.kwargs:
            project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
            projects_data = self.serializer_class(project).data
            return Response(projects_data)
        else:
            projects = Project.objects.all()
            projects_data = self.serializer_class(projects, many=True).data
            return Response(projects_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, *args, pk, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        project.delete()
        return JsonResponse({'message': 'Проект удалён'})

