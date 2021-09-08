from django.urls import path, include
from .views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsCreateView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    TasksUpdateView,
    TasksDeleteView,
    TaskNotifs,
    CommentNotifs
)
from projects import views as project_views

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects-home'),
    path('<int:pk>/',ProjectsDetailView.as_view(), name= 'projects-detail'),
    path('new/',ProjectsCreateView.as_view(), name= 'projects-create'),
    path('<int:pk>/update/',ProjectsUpdateView.as_view(), name= 'projects-update'),
    path('<int:pk>/delete/',ProjectsDeleteView.as_view(), name= 'projects-delete'),
    #path('<int:pk>/', TaskListView.as_view,name='projects-tasks'),
    #path('<int:pk>/tasks/new/',project_views.addTask,name='tasks-create'),
    path('<int:pk>/add-task', project_views.addTask, name="tasks-create"),
    path('<int:pk>/complete-task', project_views.completeTask, name="tasks-complete"),
    path('<int:pk>/tasks/update/',TasksUpdateView.as_view(),name='tasks-update'),
    path('<int:pk>/tasks/delete/',TasksDeleteView.as_view(),name='tasks-delete'),
    path('notification/<int:notif_pk>/task/<int:task_pk>', TaskNotifs.as_view(), name='task-notif'),
    path('<int:pk>/write-comment', project_views.write_comment, name="comment-create"),
    path('notification/<int:notif_pk>/comment/<int:project_pk>', CommentNotifs.as_view(), name='comment-notif'),
]