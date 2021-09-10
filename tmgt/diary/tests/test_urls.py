from django.test import SimpleTestCase
from django.urls import reverse, resolve
from diary.views import (
    EntryListView,
    EntryCreateView,
    EntryDetailView,
    EntryUpdateView,
    EntryDeleteView,
    addEntry
)

class TestUrls(SimpleTestCase):

    # Success
    def test_entry_list_is_resolved(self):
        url = reverse('diary-home', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EntryListView)

    # Success
    def test_entry_create_is_resolved(self):
        url = reverse('entry-create')
        self.assertEquals(resolve(url).func.view_class, EntryCreateView)

    # Success
    def test_entry_detail_is_resolved(self):
        url = reverse('entry-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EntryDetailView)

    # Success
    def test_entry_update_is_resolved(self):
        url = reverse('entry-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EntryUpdateView)

    # Success
    def test_entry_delete_is_resolved(self):
        url = reverse('entry-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EntryDeleteView)

    # Success
    def test_add_entry_is_resolved(self):
        url = reverse('add-entry', args=['1'])
        self.assertEquals(resolve(url).func, addEntry)
