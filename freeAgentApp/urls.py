from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name='freeAgentApp'

urlpatterns = [

    # /freeAgentApp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /freeAgentApp/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # /freeAgentApp/login
    url(r'^login/$', views.Login.as_view(), name='login'),
    # /freeAgentApp/logout
    url(r'^logout/$', views.LogOut.as_view(), name='logout'),
    # /freeAgentApp/13/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /freeAgentApp/project/add/
    url(r'project/add/$', views.ProjectCreate.as_view(), name='createProject'),
    # /freeAgentApp/upload
    url(r'project/upload/(?P<pk>[\w-]+)$', views.ProjectUpload.as_view(), name='Upload'),
    # /freeAgentApp/project/2/
    url(r'project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='updateProject'),
    # /freeAgentApp/project/2/delete/
    url(r'project/(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name='deleteProject'),
    # /freeAgent/workerIndex
    url(r'^workerIndex/$', views.WorkerView.as_view(), name='workerIndex'),
    # /freeAgent/addWorker
    url(r'^addWorker/$', views.add_worker, name='addWorker'),
    # /freeAgent/serializerUsername
    url(r'^serializerUsername', views.UserSerializer.as_view(), name='userNameSerializer'),
    # ／freeAgentApp/SerializeProject/create
    url(r'^serializerProject/create', views.ProjectCreateAPI.as_view(), name='ProjectCreateSerializer'),
    # ／freeAgentApp/SerializeProject/manage
    url(r'^serializerProject/manage/(?P<pk>[0-9]+)/',
        views.ProjectUpdateAndDeleteAPI.as_view(),
        name='ProjectManageSerializer'),
    # /freeAgentApp/search
    url(r'^results/$', views.search, name='search'),
    # ／freeAgentApp/SerializeProject/list
    url(r'^serializerProject/list', views.ProjectListAPI.as_view(), name='ProjectListSerializer'),
    # /freeAgentApp/homePage-public
    url(r'^homepage-public/$', views.HomePageViewAuthFalse.as_view(), name='homeAuthFalse'),
    # /freeAgentApp/homePage
    url(r'^homepage/$', views.HomePageViewAuthTrue.as_view(), name='homeAuthTrue'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
