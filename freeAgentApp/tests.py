import datetime
from django.utils import timezone
from django.test import TestCase
from freeAgentApp.models import Project,Review,UserProfile
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from django.db import models


class ProjectModelTests(TestCase):
    
    client = Client()
    
    # def user_is_unique(self):
        # """user_is_unique() returns False for user registration if username is not unique."""
       
    def test_user_is_logged_in(self):
        """Checks that user is redirected to login page if not in a current session"""
        response = self.client.get(reverse('freeAgentApp:index'))
        self.assertEqual(response.status_code, 302)

