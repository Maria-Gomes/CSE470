from django.test import SimpleTestCase
from django.urls import reverse, resolve
from projects.views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsCreateView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    addTask,
    completeTask,
    write_comment,
    TasksUpdateView,
    TasksDeleteView,
    TaskNotifs,
    CommentNotifs
)

class TestUrls(SimpleTestCase):

    # Success
    def test_proj_list_is_resolved(self):
        url = reverse('projects-home')
        self.assertEquals(resolve(url).func.view_class, ProjectsListView)

    # Success
    def test_proj_detail_is_resolved(self):
        url = reverse('projects-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProjectsDetailView)

    # Success
    def test_proj_create_is_resolved(self):
        url = reverse('projects-create')
        self.assertEquals(resolve(url).func.view_class, ProjectsCreateView)

    # Success
    def test_proj_update_is_resolved(self):
        url = reverse('projects-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProjectsUpdateView)

    # Success
    def test_proj_delete_is_resolved(self):
        url = reverse('projects-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProjectsDeleteView)

    # Success
    def test_task_update_is_resolved(self):
        url = reverse('tasks-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TasksUpdateView)

    # Success
    def test_task_delete_is_resolved(self):
        url = reverse('tasks-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TasksDeleteView)

    # Success
    def test_task_notif_is_resolved(self):
        url = reverse('task-notif', args=['1', '1'])
        self.assertEquals(resolve(url).func.view_class, TaskNotifs)

    # Success
    def test_comment_notif_is_resolved(self):
        url = reverse('comment-notif', args=['1', '1'])
        self.assertEquals(resolve(url).func.view_class, CommentNotifs)

    # Success
    def test_add_task_is_resolved(self):
        url = reverse('tasks-create', args=['1'])
        self.assertEquals(resolve(url).func, addTask)

    # Success
    def test_complete_task_is_resolved(self):
        url = reverse('tasks-complete', args=['1'])
        self.assertEquals(resolve(url).func, completeTask)

    # Success
    def test_write_comment_is_resolved(self):
        url = reverse('comment-create', args=['1'])
        self.assertEquals(resolve(url).func, write_comment)
