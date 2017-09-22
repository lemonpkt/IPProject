from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Project, Member, Review
from django.views import generic



class accepted_projects(generic.ListView):
    template_name='accepted_projects.html'
    model=Project
    
    def get_queryset(self):
        """Returns accepted Projects that belong to the current user"""
        return Project.objects.filter(user=self.request.user_name,statsu=2).order_by('project_id')
                   
            
class all_projects(generic.ListView):
    template_name='templates/all_projects.html'
    model=Project
    
    def get_queryset(self):
        """Return all projects"""
        return Project.objects.order_by("pub_date")
    
    
class create_project(generic.ListView):
    template_name='templates/create_project.html'   
    model=Project
    
    
    
    
class end_client_projects(generic.ListView):
    template_name='templates/end_client_projects.html'
    model=Project
    
    def get_queryset(self):
        """Return all proejcts owned by a client"""
        return Project.objects.filter(client.self)
    
    
class login(generic.ListView):
    template_name='templates/login.html'
    model=Member
    
    
    
class register(generic.ListView):
    template_name='templates/register.html'
    model=Member