from django.db import models
import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator 
from decimal import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,AbstractUser


class UserProfile(AbstractUser):
    
    Identification = models.CharField(max_length=10, choices=(('F', 'freeAgent'), ('C', 'Client')))


class Project(models.Model):

    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    pub_date = timezone.now()

    # Status could be one of four. (New=1, Applied=2, Accepted && Working=3, Completed && Closed=4)
    status = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    description = models.CharField(max_length=300)
    file_type = models.FileField(null=True, blank=True)
    client_upload = models.FileField(null=True, blank=True)
    client = models.ForeignKey(UserProfile, related_name="ThisClient", null=True, blank=True)
    worker = models.ForeignKey(UserProfile, related_name="ThisWorker", null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('freeAgentApp:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s" % self.title
        
        
class Review(models.Model):
    
    # Client can only enter an integer between 0 & 10
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    project_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return "%s" % self.project_rating
