from django.urls import path
from .views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsCreateView,
    ProjectsUpdateView,
    ProjectsDeleteView
)
from . import views

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects-home'),
    path('<int:pk>/',ProjectsDetailView.as_view(), name= 'projects-detail'),
    path('new/',ProjectsCreateView.as_view(), name= 'projects-create'),
    path('<int:pk>/update/',ProjectsUpdateView.as_view(), name= 'projects-update'),
    path('<int:pk>/delete/',ProjectsDeleteView.as_view(), name= 'projects-delete')
]