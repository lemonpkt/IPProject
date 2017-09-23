from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator 
from decimal import *

##Note:Category Client=True
class Member(models.Model):
    user_name = models.CharField(primary_key=True, max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    category = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.first_name



class Project(models.Model):
    def creation_date(self):
        return self.pub_date
            
    def __str__(self):
        return self.title + ' (' + str(self.status) + ')'

    project_id = models.IntegerField(primary_key=True)

    # related_name='+' means there is no reverse accessor on Member
    # i.e. We cannot write m.project_set.all() for some Member object `m`
    client = models.ForeignKey(Member, related_name='+')
    worker = models.ForeignKey(Member, related_name='+')
    
    
    # Status could be one of four. (New=1, Accdepted=2, completed=3 & closed=4)
    status = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    
    description = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=30, decimal_places=15)
    pub_date = models.DateTimeField('date created')
    code = models.FileField(upload_to='uploads/')

class Review(models.Model):
    project_id = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    
    #Client can only enter an integer between 0 & 10
    project_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return "Review {}/10".format((self.project_rating, ))
