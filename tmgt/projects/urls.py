from django.urls import path
from .views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsCreateView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    #TasksUpdateView,
    TasksDeleteView
)
from projects import views as project_views

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects-home'),
    path('<int:pk>/',ProjectsDetailView.as_view(), name= 'projects-detail'),
    path('new/',ProjectsCreateView.as_view(), name= 'projects-create'),
    path('<int:pk>/update/',ProjectsUpdateView.as_view(), name= 'projects-update'),
    path('<int:pk>/delete/',ProjectsDeleteView.as_view(), name= 'projects-delete'),
    #path('<int:pk>/', TaskListView.as_view,name='projects-tasks'),
    path('<int:pk>/tasks/new/',project_views.addTask,name='tasks-create'),
    path('<int:pk>/tasks/update/',project_views.editTask,name='tasks-update'),
    path('<int:pk>/tasks/delete/',TasksDeleteView.as_view(),name='tasks-delete')
]