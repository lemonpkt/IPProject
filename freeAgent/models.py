# Up to opening second python shell
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator, MaxValueValidator 
from decimal import *


from django.core.files.storage import FileSystemStorage
##TODO:fs=FileSystemStorage(location='https://docs.djangoproject.com/en/1.11/topics/files/')
##This is required for the project_details class




# Create your models here.
@python_2_unicode_compatible
class member(models.Model):


	user_name= models.CharField(primary_key=True,max_length=50)
	email=models.CharField(max_length=50,unique=True)
	password=models.CharField(max_length=50)
	category=models.BooleanField(default=True)
	first_name=models.CharField(max_length=30)
	last_name=models.CharField(max_length=30)
	
	def __str__(self):
		return self.first_name
		
	def __str__(self):
		return self.category


class client(models.Model):

	def __str__(self):
		return self.user_name
	
	user_name= models.ForeignKey(member, on_delete=models.CASCADE)
	

class worker (models.Model):

	def __str__(self):
		return self.user_name
		
	def __str__(self):
		return self.average_rating
		
	user_name=models.ForeignKey(member, on_delete=models.CASCADE)
##TODO:Need to work out how average rating will be constructed
##average_rating


class project(models.Model):

	def __int____(self):
		return self.project_id
		
	def __str__(self):
		return self.client
		
	def __str__(self):
		return self.worker
	
	project_id=models.IntegerField(primary_key=True)
##TODO: Can you guys check if this is the correct contect for calling the client/worker? I had to comment them out as it was causing an error	
	##client=models.user_name.ForeignKey(member)
	##worker=models.user_name.ForeignKey(member)


class review(models.Model):

	
	def __int__(self):
		return self.project_rating
	
	project_id=models.OneToOneField(project, on_delete=models.CASCADE,primary_key=True)
	
	#Client can only enter an integer between 0 & 10
	project_rating=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

	
class payment_transaction (models.Model):

	def __int__(self):
		return self.transaction_id
	
	transaction_id=models.IntegerField(primary_key=True)
	project_id=models.ForeignKey(review, on_delete=models.CASCADE)
	user_name=models.ForeignKey(member, on_delete=models.CASCADE)
	
	
	
class project_details (models.Model):

	def creation_date(self):
		return self.pub_date
		
	def __str__(self):
		return self.description
		
	def __str__(self):
		return self.title
	
	def __str__(self):
		return self.date_time
	
	def __int__(self):
		return self.status
	
	#Status could be one of four. (New=1, started=2, completed=3 & closed=4)
	status=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
	
	project_id=models.ForeignKey(project, on_delete=models.CASCADE)
	description=models.CharField(max_length=300)
	title=models.CharField(max_length=100)
	date_time=models.DateTimeField('date created')
	
##Looking at the ER diagram we need to workout what we maen by "codeBase" & "filePath"
##TODO:	code_base=models.FileField(upload_to='?????????????')
##TODO:	cost= (Possibly use a deciimal field here??? https://docs.python.org/3/library/decimal.html#module-decimal)
	
	