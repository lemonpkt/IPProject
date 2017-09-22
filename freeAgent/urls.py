from django.conf.urls import url
from . import views

app_name='freeAgent'

urlpatterns = [
    url(r'^accepted_projects$', views.accepted_projects.as_view(), name='accepted_projects'),
    url(r'^all_projects$', views.all_projects.as_view(), name='all_projects'),
    url(r'^create_projects$', views.create_project.as_view(), name='create_project'),
    url(r'^end_client_projects$', views.end_client_projects.as_view(), name='end_client_projects'),
    url(r'^$', views.login.as_view(), name='login'),
    url(r'^register$', views.register.as_view(), name='register')

    
]
