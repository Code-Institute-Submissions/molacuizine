from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.models import User
from checkout.models import Order
from .models import Town


# Create your tests here.
class ProfileTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        self.Town = Town.objects.create(
            name="vacoas", long_coord=-20.3171, lat_coord=57.5265)

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

    def test_order_history_page(self):
        order = Order.objects.create(
            full_name='zahur meerun',
            email='zahurmeerun@yahoo.com',
            phone_number='57075200',
            street_address='vacoas',
            town=get_object_or_404(
                        Town, name='vacoas'),
            postcode='222222',
            request='none')
        response = self.client.get(
            f'/profile/order_history/{order.order_number}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/order_history.html')
