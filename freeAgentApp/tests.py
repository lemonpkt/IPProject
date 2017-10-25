from django.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse

from freeAgentApp.models import Project, Review, UserProfile
from freeAgentApp.views import ProjectCreate

class LoginTests(TestCase):
    
    client = Client()
    
    def test_required_login(self):
        """Checks that user is redirected to login page if not in a current session"""

        response = self.client.get(reverse('freeAgentApp:index'))
        self.assertEqual(response.status_code, 302)

    def test_user_registration(self):
        """Checks a user account can be registered."""

        response = self.client.post(reverse('freeAgentApp:register'),
                {'username': 'cool_dude',
                'password': 'cooldude123',
                'email': 'cool@email.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'Identification': 'C'})

        # Redirect on successful registration
        self.assertEqual(response.status_code, 302)

    def test_register_unique_username(self):
        """Checks that a user can't create an account with a username which
        is already taken.
        
        """

        username = 'unique_username'

        user = UserProfile.objects.create(username=username)
        user.save()

        response = self.client.post(reverse('freeAgentApp:register'),
                {'username': username,
                'password': 'password123'})

        # Not redirected to index page means registration failed
        self.assertNotEqual(response.status_code, 302)


class ClientTests(TestCase):
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

        # Check that there is a new Project in the db pointing to self.user
        self.assertEqual(len(Project.objects.filter(client=self.user)), 1)
