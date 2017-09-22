from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accepted_projects$', views.accepted_projects, name='accepted_projects'),
    url(r'^all_projects$', views.all_projects, name='all_projects'),
    url(r'^create_projects$', views.create_project, name='create_project'),
    url(r'^end_client_projects$', views.end_client_projects, name='end_client_projects'),
    url(r'^$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    
]
