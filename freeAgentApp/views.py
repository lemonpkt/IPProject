from django.views import generic
from .models import Project,Review,UserProfile
from django.views.generic import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, render_to_response
from django.contrib.auth import authenticate,login
#from django.views.generic import View
from .forms import UserForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProjectSerializer,ReviewSerializer, UserProfileSerializer
from django.contrib.auth.models import User,AbstractUser
import re
from django.db.models import Q
   
def add_worker(request):
    if request.method == "POST":    
        if 'add' in request.POST:
                      
            user = request.user
            project = Project.objects.get(id=request.POST["project.id"])
            project.worker = user
            project.save()            
        return redirect('freeAgentApp:workerIndex') 
    return redirect('freeAgentApp:index')
 
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string into invidual keywords, getting rid of unecessary spaces '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        print ('Query String is ' + query_string)
        entry_query = get_query(query_string, ['title','description',])
        found_entries = Project.objects.filter(entry_query).order_by('id')
        print (found_entries)
        
    return render(request,'freeAgentApp/results.html',{'found_entries':found_entries})
                                         
                          
class UserFormView(View):
    form_class=UserForm
    template_name='freeAgentApp/registration.html'

    #New form
    def get(self,request):
        if request.user.is_authenticated():
            return redirect('freeAgentApp:index')

        form = self.form_class()
        return render(request, self.template_name,{'form':form})

        
    #Completed form
    def post(self,request):
        form =self.form_class(request.POST)
           
        if form.is_valid():
           
            user=form.save(commit=False)
                
            #Get cleaned noramlised data - i.e. date entries etc
            username=form.cleaned_data['username']
            password= form.cleaned_data['password']
            try:
                UserProfile.objects.get(username=username)

                #Change user password
            except UserProfile.DoesNotExist:
                user.set_password(password)
                user.save()

                #This retruns the USer objects if authentication is correct
                user=authenticate(username=username,password=password)

                if user is not None:
                    if user.is_active:
                        login(request,user)

                            #request.user.username
                            #request.user.email
                    return redirect('freeAgentApp:index')
                return render(request,self.template_name,{'form':form})

        return render(request, self.template_name, {'form': form})

                        

class IndexView(LoginRequiredMixin, generic.ListView ):
    template_name='freeAgentApp/index.html'
    
    def get_queryset(self):
        # Filter by username if the type of user is client
        user = self.request.user
        if user.Identification == 'C':
            return Project.objects.filter(client=user)
        else:
            return Project.objects.all()
    
      
      
class WorkerView(LoginRequiredMixin, generic.ListView ):
    print("Debug1")
    model=Project
    template_name='freeAgentApp/workerIndex.html'  
  
    def get_queryset(self):
        # Filter by username if the type of user is client
      
        user = self.request.user
        return Project.objects.filter(worker=user)
        
       
class DetailView(LoginRequiredMixin,generic.DetailView):
    model=Project
    template_name='freeAgentApp/detail.html'
    
class ProjectCreate(LoginRequiredMixin,CreateView):
    model=Project
    fields=['title','cost','description','status','file_type']

    def form_valid(self, form):
        """Called when a form is valid and a new project is about to be saved."""
        # Calls default form_valid() method and saves a new project in self.object
        response = super(ProjectCreate, self).form_valid(form)

        # Set the project's client (the user that created the project) to be the current user
        self.object.client = self.request.user
        self.object.save()

        # Required by the CreateView view to return the reponse objects
        return response

class ProjectUpdate(UpdateView):
    model=Project
    fields=['title','cost','description','status']
 
           
             
class ProjectDelete(DeleteView):
    model=Project
    success_url = reverse_lazy('freeAgentApp:index')


class Login(LoginView):
    form_class = LoginForm
    template_name = "freeAgentApp/login.html"
    redirect_authenticated_user = True



class LogOut(LogoutView):
    # next_page = 'login'
    pass


