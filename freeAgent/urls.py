from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.accepted_projects, name='accepted_projects'),
    url(r'^$', views.all_projects, name='all_projects'),
    url(r'^$', views.create_project, name='create_project'),
    url(r'^$', views.end_client_projects, name='end_client_projects'),
    url(r'^$', views.login, name='login'),
    url(r'^$', views.register, name='register'),
    
]