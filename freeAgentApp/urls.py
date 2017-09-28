from django.conf.urls import url
from . import views

app_name='freeAgentApp'

urlpatterns = [
    
    #/freeAgentApp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #/freeAgentApp/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/freeAgentApp/13/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='detail'),
    #/freeAgentApp/project/add/
    url(r'project/add/$',views.ProjectCreate.as_view(), name='createProject'),
    #/freeAgentApp/project/2/
    url(r'project/(?P<pk>[0-9]+)/$',views.ProjectUpdate.as_view(), name='updateProject'),
    #/freeAgentApp/project/2/delete/
    url(r'project/(?P<pk>[0-9]+)/delete/$',views.ProjectDelete.as_view(), name='deleteProject'),
    
]