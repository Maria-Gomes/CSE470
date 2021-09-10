from django.test import TestCase, Client
from projects.models import Projects, Tasks, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')


    def test_proj_create(self):
        proj = Projects.objects.create(pk=1, title='Title', about='About', date_posted=timezone.now(), author=self.user, progress=0.0)
        self.assertTrue(isinstance(proj, Projects))
        self.assertEqual(proj.title, 'Title')

    def test_url(self):
        self.client.login(username='john', password='johnpassword')
        proj = Projects.objects.create(pk=1, title='Title', about='About', date_posted=timezone.now(), author=self.user,
                                       progress=0.0)
        response = self.client.get(reverse('projects-detail', args=[proj.pk]))
        self.assertEquals(response.status_code, 200)