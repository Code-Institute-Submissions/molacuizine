from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse
from django.contrib.auth.models import User


# Create your tests here.
class CheckoutTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')

    def test_cache_checkout_data(self):
        secret = 'pi_1IBzdcL9RkpyhrRPuVMAEiDc_secret_6GvTfYgq8m2imeAdHFQ2Byv4a'
        post_data = {
            'client_secret': secret,
            'save_info': 'saveInfo',
            'request': '',
        }
        response = self.client.post(reverse('cache_checkout_data'), post_data)
        self.assertEqual(response.status_code, 200)

    def test_cache_checkout_data_erroneous_data(self):
        secret = 'pi_1IBzdcL9RkpyhrRPuVMAEiDc_secret_6GvTfYgq8m2imeAdHFQ2Byv4a'
        post_data = {
            'xxxxx': secret,
            'save_info': 'saveInfo',
            'request': 'requestInfo',
        }
        response = self.client.post(reverse('cache_checkout_data'), post_data)
        self.assertEqual(response.status_code, 400)

    def test_cache_checkout_data_with_buyer_request(self):
        secret = 'pi_1IBzdcL9RkpyhrRPuVMAEiDc_secret_6GvTfYgq8m2imeAdHFQ2Byv4a'
        post_data = {
            'client_secret': secret,
            'save_info': 'saveInfo',
            'request': 'i hava a request',
        }
        response = self.client.post(reverse('cache_checkout_data'), post_data)
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        login = self.client.login(
            username='testuser', password='zahur')
        bag = self.client.session.get('bag', {})
        response = self.client.post(reverse('checkout'))
        self.assertEqual(len(bag), 0)
        self.assertRedirects(response, '/products/')
