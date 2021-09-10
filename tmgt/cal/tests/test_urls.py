from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cal.views import (
    EventListView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    EventNotifs,
    addEvent
)

class TestUrls(SimpleTestCase):

    # Success
    def test_event_list_is_resolved(self):
        url = reverse('calendar-home', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventListView)

    # Success
    def test_event_detail_is_resolved(self):
        url = reverse('event-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventDetailView)

    # Success
    def test_event_update_is_resolved(self):
        url = reverse('event-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventUpdateView)

    # Success
    def test_event_delete_is_resolved(self):
        url = reverse('event-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventDeleteView)

    # Success
    def test_event_notif_is_resolved(self):
        url = reverse('event-notif', args=['1', '1'])
        self.assertEquals(resolve(url).func.view_class, EventNotifs)

    # Success
    def test_add_event_is_resolved(self):
        url = reverse('event-create')
        self.assertEquals(resolve(url).func, addEvent)