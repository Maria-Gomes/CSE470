from django.urls import path, include
from .views import (
    EventListView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    EventNotifs
)
from cal import views as cal_views

urlpatterns = [
    path('<int:pk>/', EventListView.as_view(), name='calendar-home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('add-event/', cal_views.addEvent, name='event-create'),
    path('<int:pk>/update/',EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/',EventDeleteView.as_view(), name='event-delete'),
    path('notification/<int:notif_pk>/event/<int:event_pk>', EventNotifs.as_view(), name='event-notif')
]