from django.test import TestCase
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class TestProductModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')

    def test_item_string_returns_names(self):
        userprofile = get_object_or_404(UserProfile, user__username='testuser')
        self.assertAlmostEqual(str(userprofile), 'testuser')
