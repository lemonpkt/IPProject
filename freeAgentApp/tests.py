from django.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse

from freeAgentApp.models import Project, Review, UserProfile
from freeAgentApp.views import ProjectCreate

class ProjectModelTests(TestCase):
    
    client = Client()
    
    # def user_is_unique(self):
        # """user_is_unique() returns False for user registration if username is not unique."""
       
    def test_user_is_logged_in(self):
        """Checks that user is redirected to login page if not in a current session"""
        response = self.client.get(reverse('freeAgentApp:index'))
        self.assertEqual(response.status_code, 302)


class ClientCreateProjectTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfile.objects.get_or_create(username='test_user')[0]

        # Create a logged-in client
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_project(self):
        """Checks that when a client creates a new project they are added as
        the owner of that project.

        """
        # Send a form to the createProject page
        response = self.client.post(reverse('freeAgentApp:createProject'),
                {'title': "My Cool Project",
                    'cost': '999.50',
                    'description': "This is a cool project for cool dudes.",
                    'file_type': ''})
        #self.assertEqual(response.status_code, 200)

        # Check that there is a new Project in the db pointing to self.user
        self.assertEqual(len(Project.objects.filter(client=self.user)), 1)
