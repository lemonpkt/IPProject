from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name='freeAgentApp'

urlpatterns = [
    
    #/freeAgentApp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #/freeAgentApp/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/freeAgentApp/login
    url(r'^login/$',views.Login.as_view(), name='login'),
    #/freeAgentApp/logout
    url(r'^logout/$',views.LogOut.as_view(), name='logout'),
    #/freeAgentApp/13/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='detail'),
    #/freeAgentApp/project/add/
    url(r'project/add/$',views.ProjectCreate.as_view(), name='createProject'),
    #/freeAgentApp/project/2/
    url(r'project/(?P<pk>[0-9]+)/$',views.ProjectUpdate.as_view(), name='updateProject'),
    #/freeAgentApp/project/2/delete/
    url(r'project/(?P<pk>[0-9]+)/delete/$',views.ProjectDelete.as_view(), name='deleteProject'),
    #/freeAgentApp/workerIndex
    url(r'^workerIndex/$',views.WorkerView.as_view(), name='workerIndex'),
    #/freeAgentApp/addWorker
    url(r'^addWorker/$',views.add_worker, name='addWorker'),
    #/freeAgentApp/results
    url(r'^results/$',views.search_view,name='results'),
    #/freeAgentApp/search
    #url(r'^search/$',views.search_view.search,name='search'),
]



urlpatterns =  format_suffix_patterns(urlpatterns)