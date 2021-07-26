from django.urls import path
from .views import (
    EntryListView,
    EntryCreateView,
    EntryDetailView,
    EntryUpdateView,
    EntryDeleteView
)
from diary import views as diary_views

urlpatterns = [
    path('<int:pk>/', EntryListView.as_view(), name='diary-home'),
    path('new/entry/',EntryCreateView.as_view(), name='entry-create'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='entry-detail'),
    path('<int:pk>/update/',EntryUpdateView.as_view(), name= 'entry-update'),
    path('<int:pk>/delete/',EntryDeleteView.as_view(), name= 'entry-delete'),
]