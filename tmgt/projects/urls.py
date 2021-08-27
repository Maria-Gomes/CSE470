from django.urls import path, include
from .views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsCreateView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    TasksUpdateView,
    TasksDeleteView,
    TaskNotifs
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
    path('<int:pk>/tasks/update/',TasksUpdateView.as_view(),name='tasks-update'),
    path('<int:pk>/tasks/delete/',TasksDeleteView.as_view(),name='tasks-delete'),
    path('notification/<int:notif_pk>/task/<int:task_pk>', TaskNotifs.as_view(), name='task-notif')
]