from django.test import Client, TestCase
from django.urls import reverse
from projects.models import Projects, Tasks, Comment
from django.contrib.auth.models import User
from projects.views import addTask
from datetime import datetime

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_proj_list_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('projects-home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/home.html')

    def test_proj_create(self):
        self.client.login(username='john', password='johnpassword')
        data = {
            'title': 'Title',
            'about': 'About',
        }
        self.client.post(reverse('projects-create'), data)
        self.assertEqual(Projects.objects.last().title, 'Title')

    def test_proj_create_display(self):
        self.client.login(username='john', password='johnpassword')
        proj = Projects.objects.create(pk=1, title='Title', about='About', date_posted=datetime.now(), author=self.user, progress=0.0)
        response = self.client.get(reverse('projects-detail', args=[proj.pk]))

        self.assertContains(response, 'About')

    def test_update_proj(self):
        proj = Projects.objects.create(pk=1, title='Title', about='About', date_posted=datetime.now(), author=self.user, progress=0.0)

        response = self.client.post(
            reverse('projects-update', kwargs={'pk': proj.id}),
            {'title': 'Updated Title', 'about': 'About'})

        self.assertEqual(response.status_code, 302)

    def test_proj_update_display(self):
        self.client.login(username='john', password='johnpassword')
        proj = Projects.objects.create(pk=1, title='Title', about='About', date_posted=datetime.now(), author=self.user, progress=0.0)
        data = {
            'title': 'Updated Title',
            'about': 'About',
        }
        self.client.post(reverse('projects-update', args=[proj.pk]), data)
        self.assertEqual(Projects.objects.last().title, 'Updated Title')