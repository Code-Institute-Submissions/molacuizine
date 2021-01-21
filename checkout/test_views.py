from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse
from django.contrib.auth.models import User
from products.models import Product, Category


# Create your tests here.
class CheckoutTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        self.Categoty = Category.objects.create(name="sides")

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

    def test_checkout_empty_bag(self):
        bag = self.client.session.get('bag', {})
        response = self.client.get(reverse('checkout'))
        self.assertEqual(len(bag), 0)
        self.assertRedirects(response, '/products/')

    def test_checkout_with_store_status_closed(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Create bag
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        bag = self.client.session.get('bag', {})
        response = self.client.post('/bag/store_status/', {'status': 'close'})
        response = self.client.get(reverse('checkout'))
        self.assertEqual(len(bag), 1)
        self.assertRedirects(response, '/products/')

    def test_checkout_with_store_status_open(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Create bag
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        bag = self.client.session.get('bag', {})
        response = self.client.get(reverse('checkout'))
        self.assertEqual(len(bag), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
