from django.views import generic
from .models import Project, Review, UserProfile
from django.views.generic import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseFormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProjectSerializer, ProjectCreateSerializer, UserProfileSerializer
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.db.models import Q


def add_worker(request):
    """Handles adding workers to projects and uploading code to projects.
    Called when a corresponding button is clicked on a project."""

    if request.method == "POST":    
        # Free Agent clicked 'add' button on a project
        if 'add' in request.POST:
            user = request.user
            project = Project.objects.get(id=request.POST["project.id"])

            if project.status == 1:
                project.worker = user
                project.status = 2
                project.save()
            else:
                return HttpResponseRedirect('../?message=1')
                # redirect('freeAgentApp:index')
            return redirect('freeAgentApp:workerIndex')

        # End Client accepts or rejects a Free Agent on a project
        if 'Accept' in request.POST:
            project = Project.objects.get(id=request.POST["project.id"])
            if project.status == 2:
                project.status = 3
                project.save()
            return redirect('freeAgentApp:detail', project.id)
        elif 'Refuse' in request.POST:
            project = Project.objects.get(id=request.POST["project.id"])
            project.status = 1
            project.worker = None
            project.save()
            return redirect('freeAgentApp:detail', project.id)

        # Free Agent uploads completed code submission to a project
        if 'UploadWork' in request.POST:
            project = Project.objects.get(id=request.POST["project.id"])
            project.save()
            return redirect('freeAgentApp:detail', project.id)

        # End Client confirms a completed code submission on a project
        if 'ConfirmWork' in request.POST:
            project = Project.objects.get(id=request.POST["project.id"])
            project.status = 4
            project.save()
            return redirect('freeAgentApp:detail', project.id)

    # We don't do GET requests!
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
        
    return render(request,'freeAgentApp/results.html',{'found_entries':found_entries, 'query_string':query_string,})
                                         
                          
class UserFormView(View):
    """Registration form."""
    form_class = UserForm
    template_name = 'freeAgentApp/registration.html'

    # New form
    def get(self,request):
        if request.user.is_authenticated():
            return redirect('freeAgentApp:index')

        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    # Completed form. Creates a new user.
    def post(self,request):
        form = self.form_class(request.POST)
           
        if form.is_valid():
           
            user = form.save(commit=False)
                
            # Get cleaned noramlised data - i.e. date entries etc
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Make sure the username is unique
            try:
                UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                # Change user password
                user.set_password(password)
                user.save()

                # Authenticate and login the new user
                user = authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                    return redirect('freeAgentApp:index')
                return render(request, self.template_name, {'form':form})

        # Registration failed
        return render(request, self.template_name, {'form': form})


class IndexView(LoginRequiredMixin, generic.ListView):
    """Home page. Displays a list of created projects for an End Client, and
    a list of all projects to a Free Agent.

    """
    template_name = 'freeAgentApp/index.html'

    def get_queryset(self):
        # Filter by username if the type of user is client
        user = self.request.user
        if user.Identification == 'C':
            return Project.objects.filter(client=user)
        else:
            return Project.objects.all()


class HomePageViewAuthTrue(LoginView):
    template_name = 'freeAgentApp/homeAuthTrue.html'


class HomePageViewAuthFalse(LoginView):
    template_name = 'freeAgentApp/homeAuthFalse.html'


class WorkerView(LoginRequiredMixin, generic.ListView):
    """Displays a list of all the projects an End Client has accepted."""

    model = Project
    template_name = 'freeAgentApp/workerIndex.html'
  
    def get_queryset(self):
        # Filter by username if the type of user is client
      
        user = self.request.user
        return Project.objects.filter(worker=user)
        
       
class DetailView(LoginRequiredMixin, generic.DetailView):
    """Detailed information for a given project."""

    model = Project
    template_name = 'freeAgentApp/detail.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    """Form to create a new project."""

    model = Project
    fields = ['title', 'cost', 'description', 'file_type']

    def form_valid(self, form):
        """Called when a form is valid and a new project is about to be saved."""
        # Calls default form_valid() method and saves a new project in self.object
        response = super(ProjectCreate, self).form_valid(form)

        # Set the project's client (the user that created the project) to be the current user
        self.object.client = self.request.user
        self.object.save()

        # Required by the CreateView view to return the reponse objects
        return response


class ProjectUpload(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['client_upload']


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'cost', 'description', 'status']
 

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('freeAgentApp:index')


class Login(LoginView):
    """Login page."""

    form_class = LoginForm
    template_name = "freeAgentApp/login.html"
    redirect_authenticated_user = True


class LogOut(LogoutView):
    pass


#
# RESTful API views
#

class UserSerializer(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProjectListAPI(ListAPIView):
    serializer_class = ProjectSerializer
    permissions_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.Identification is 'C':
            self.queryset = Project.objects.filter(client=user)
            return self.queryset
        elif user.Identification is 'F':
            self.queryset = Project.objects.filter(worker=user)
            return self.queryset


class ProjectCreateAPI(CreateAPIView):
    # queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permissions_class = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectUpdateAndDeleteAPI(RetrieveUpdateDestroyAPIView):
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permissions_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.Identification is 'C':
            self.queryset = Project.objects.filter(client=user)
            return self.queryset
        elif user.Identification is 'F':
            self.queryset = Project.objects.filter(worker=user)
            return self.queryset

