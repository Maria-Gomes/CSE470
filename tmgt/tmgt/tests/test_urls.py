from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
    register,
    profile,
    logout_view
)

class TestUrls(SimpleTestCase):

    # Success
    def test_register_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    # Success
    def test_profile_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    # Success
    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)