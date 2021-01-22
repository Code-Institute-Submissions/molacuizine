from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.models import User
from products.models import Product, Category
from profiles.models import Town
from checkout.models import Order


# Create your tests here.
class CheckoutTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        self.Category = Category.objects.create(name="sides")
        self.Town = Town.objects.create(
            name="vacoas", long_coord=-20.3171, lat_coord=57.5265)

    def test_cache_checkout_data(self):
        secret = 'pi_1ICHYpL9RkpyhrRPkV1I195z_secret_dUtSUFf1sx3ugZBV2yPJZPem1'
        post_data = {
            'client_secret': secret,
            'save_info': True,
            'request': '',
        }
        response = self.client.post(reverse('cache_checkout_data'), post_data)
        self.assertEqual(response.status_code, 200)

    def test_cache_checkout_data_erroneous_data(self):
        secret = 'pi_1ICHYpL9RkpyhrRPkV1I195z_secret_dUtSUFf1sx3ugZBV2yPJZPem1'
        post_data = {
            'xxxxx': secret,
            'save_info': 'saveInfo',
            'request': 'requestInfo',
        }
        response = self.client.post(reverse('cache_checkout_data'), post_data)
        self.assertEqual(response.status_code, 400)

    def test_cache_checkout_data_with_buyer_request(self):
        secret = 'pi_1ICHYpL9RkpyhrRPkV1I195z_secret_dUtSUFf1sx3ugZBV2yPJZPem1'
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
        response = self.client.get(reverse('checkout'))
        bag = self.client.session.get('bag', {})
        self.assertEqual(len(bag), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_order_form_valid_with_spice_index(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Create bag
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        response = self.client.get(reverse('checkout'))
        bag = self.client.session.get('bag', {})
        data = {
            'save_info': False,
            'client_secret': 'client_12345_secret_12345',
            'user_profile': 'zahur meerun',
            'full_name': 'zahur meerun',
            'email': 'zahurmeerun@yahoo.com',
            'phone_number': '57075200',
            'street_address': 'vacoas',
            'town': '1',
            'post_code': '222222',
            'request': 'none',
        }
        response = self.client.post(reverse(
            'checkout'), data=data)
        self.assertEqual(len(bag), 1)
        self.assertEqual(response.status_code, 302)

    def test_checkout_order_form_valid_without_spice_index(self):
            product = Product.objects.create(
                    name="Item", price=50, category_id=1, spice_index=True)
            # Create bag
            post_data = {
                'quantity': '1',
            }
            response = self.client.post(reverse(
                'add_to_bag', args=[product.id]), data=post_data)
            response = self.client.get(reverse('checkout'))
            bag = self.client.session.get('bag', {})
            data = {
                'save_info': False,
                'client_secret': 'client_12345_secret_12345',
                'user_profile': 'zahur meerun',
                'full_name': 'zahur meerun',
                'email': 'zahurmeerun@yahoo.com',
                'phone_number': '57075200',
                'street_address': 'vacoas',
                'town': '1',
                'post_code': '222222',
                'request': 'none',
            }
            response = self.client.post(reverse(
                'checkout'), data=data)
            self.assertEqual(len(bag), 1)
            self.assertEqual(response.status_code, 302)

    def test_checkout_order_form_invalid(self):
            product = Product.objects.create(
                    name="Item", price=50, category_id=1, spice_index=True)
            # Create bag
            post_data = {
                'quantity': '1',
            }
            response = self.client.post(reverse(
                'add_to_bag', args=[product.id]), data=post_data)
            response = self.client.get(reverse('checkout'))
            bag = self.client.session.get('bag', {})
            data = {
                'save_info': False,
                'client_secret': 'client_12345_secret_12345',
                'user_profile': 'zahur meerun',
                'full_name': 'zahur meerun',
                'email': 'zahurmeerun@yahoo.com',
                'phone_number': '57075200',
                'street_address': 'vacoas',
                'town': 'xxxxx',
                'post_code': '222222',
                'request': 'none',
            }
            response = self.client.post(reverse(
                'checkout'), data=data)
            self.assertEqual(len(bag), 1)
            self.assertRedirects(response, '/checkout/')

    def test_checkout_order_form_save_info(self):
            product = Product.objects.create(
                    name="Item", price=50, category_id=1, spice_index=True)
            # Create bag
            post_data = {
                'quantity': '1',
            }
            response = self.client.post(reverse(
                'add_to_bag', args=[product.id]), data=post_data)
            response = self.client.get(reverse('checkout'))
            bag = self.client.session.get('bag', {})
            data = {
                'save-info': True,
                'client_secret': 'client_12345_secret_12345',
                'user_profile': 'zahur meerun',
                'full_name': 'zahur meerun',
                'email': 'zahurmeerun@yahoo.com',
                'phone_number': '57075200',
                'street_address': 'vacoas',
                'town': '1',
                'post_code': '222222',
                'request': 'none',
            }
            response = self.client.post(reverse(
                'checkout'), data=data)
            self.assertEqual(len(bag), 1)
            self.assertEqual(response.status_code, 302)

    def test_checkout_success(self):
        product = Product.objects.create(
                    name="Item", price=50, category_id=1, spice_index=True)
        # Create bag
        post_data = {
            'quantity': '1',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        bag = self.client.session.get('bag', {})
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
            reverse('checkout_success',
                    args=[order.order_number]))
        self.assertEqual(len(bag), 1)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
