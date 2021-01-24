from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')

    def test_profile_page(self):
        response = self.client.get(reverse('profile'))        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_page_with_valid_update_form(self):
        data = {
            'username': 'new user name',
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')

    def test_profile_page_with_invalid_update_form(self):
        data = {
            'username': 'new user name',
            'town': 'not valid',
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')
