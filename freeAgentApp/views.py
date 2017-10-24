from django.views import generic
from .models import Project, Review, UserProfile
from django.views.generic import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

   
def add_worker(request):
    if request.method == "POST":    
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
    return redirect('freeAgentApp:index')
 

class UserFormView(View):
    form_class = UserForm
    template_name = 'freeAgentApp/registration.html'

    # New form
    def get(self,request):
        if request.user.is_authenticated():
            return redirect('freeAgentApp:index')

        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    # Completed form
    def post(self,request):
        form = self.form_class(request.POST)
           
        if form.is_valid():
           
            user = form.save(commit=False)
                
            # Get cleaned noramlised data - i.e. date entries etc
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                UserProfile.objects.get(username=username)

                # Change user password
            except UserProfile.DoesNotExist:
                user.set_password(password)
                user.save()

                # This retruns the USer objects if authentication is correct
                user = authenticate(username=username,password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)

                            # request.user.username
                            # request.user.email
                    return redirect('freeAgentApp:index')
                return render(request, self.template_name, {'form':form})

        return render(request, self.template_name, {'form': form})


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'freeAgentApp/index.html'

    def get_queryset(self):
        # Filter by username if the type of user is client
        user = self.request.user
        if user.Identification == 'C':
            return Project.objects.filter(client=user)
        else:
            return Project.objects.all()
    

class WorkerView(LoginRequiredMixin, generic.ListView ):
    print("Debug1")
    model = Project
    template_name = 'freeAgentApp/workerIndex.html'
  
    def get_queryset(self):
        # Filter by username if the type of user is client
      
        user = self.request.user
        return Project.objects.filter(worker=user)
        
       
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'freeAgentApp/detail.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
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


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'cost', 'description', 'status']
 

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('freeAgentApp:index')


class Login(LoginView):
    form_class = LoginForm
    template_name = "freeAgentApp/login.html"
    redirect_authenticated_user = True


class LogOut(LogoutView):
    # next_page = 'login'
    pass


class UserSerializer(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProjectListAPI(ListAPIView):
    serializer_class = ProjectSerializer
    prermissions_class = [permissions.IsAuthenticated]

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
        serializer.save(user = self.request.user)


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

