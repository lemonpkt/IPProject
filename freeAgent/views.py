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


##Not sure about the use of DetailView Vs ListView. 
##Documentation says DetailView is for when we want to add specifics to the table.
class accepted_projects(generic.ListView):
    template_name='accepted_projects.html'
    model=Project
    
class all_projects(generic.ListView):
    template_name='all_projects.html'
    model=Project
    
class create_project(generic.ListView):
    template_name='create_project.html'   
    model=Project
    
class end_client_projects(generic.ListView):
    template_name='end_client_projects.html'
    model=Project
    
class login(generic.ListView):
    template_name='login.html'
    model=Member
    
class register(generic.ListView):
    template_name='register.html'
    model=Member
