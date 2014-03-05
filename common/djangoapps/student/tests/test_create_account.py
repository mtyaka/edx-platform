from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from user_api.models import UserPreference
from lang_pref import LANGUAGE_KEY


class TestCreateAccount(TestCase):
    def setUp(self):
        self.username = "test_user"
        self.url = reverse("create_account")
        self.params = {
            "username": self.username,
            "email": "test@example.org",
            "password": "testpass",
            "name": "Test User",
            "honor_code": "true",
            "terms_of_service": "true",
        }

    @override_settings(LANGUAGE_CODE="eo")
    def test_default_lang_pref_saved(self):
        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username=self.username)
        self.assertEqual(UserPreference.get_preference(user, LANGUAGE_KEY), "eo")

    def test_header_lang_pref_saved(self):
        response = self.client.post(self.url, self.params, HTTP_ACCEPT_LANGUAGE="eo")
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username=self.username)
        self.assertEqual(UserPreference.get_preference(user, LANGUAGE_KEY), "eo")
