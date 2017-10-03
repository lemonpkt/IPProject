from django.views import generic
from .models import Project,Review
from django.views.generic import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm

class UserFormView(View):
    form_class=UserForm
    template_name='freeAgentApp/registration.html'

    #New form
    def get(self,request):
        form=self.form_class(None)
        return render(request, self.template_name,{'form':form})
            
        
        
    #Completed form
    def post(self,request):
        form =self.form_class(request.POST)
           
        if form.is_valid():
           
            user=form.save(commit=False)
                
            #Get cleaned noramlised data - i.e. date entries etc
            username=form.cleaned_data['username']
            password= form.cleaned_data['password']
                
            #Change user password
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
                        
                
            


class IndexView(generic.ListView):
    template_name='freeAgentApp/index.html'
    
    def get_queryset(self):
        return Project.objects.all()
        
class DetailView(generic.DetailView):
    model=Project
    template_name='freeAgentApp/detail.html'
    
class ProjectCreate(CreateView):
    model=Project
    fields=['title','cost','description','status','file_type']

class ProjectUpdate(UpdateView):
    model=Project
    fields=['title','cost','description','status','pub_date']
    
class ProjectDelete(DeleteView):
    model=Project
    success_url = reverse_lazy('freeAgentApp:index')