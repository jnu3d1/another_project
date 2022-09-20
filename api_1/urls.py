from django.urls import path, include

from api_1.views import projects_view, get_token_view, echo_view

app_name = 'api_1'

projects_urls = [
    path('', projects_view),
]

urlpatterns = [
    path('echo/', echo_view),
    path('get-token/', get_token_view),
    path('projects/', include(projects_urls)),
]
