from django.test import TestCase
from bag.models import Store
from products.models import Product, Category
from django.shortcuts import reverse, get_object_or_404


# Create your tests here.
class BagTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.Category = Category.objects.create(name='sides')

    def test_view_bag(self):
        response = self.client.get('/bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    """ Test adding items to bag """
    def test_add_to_bag(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        bag = self.client.session.get('bag', {})
        data = post_data['spice_index']
        self.assertEqual(
            bag['1']['spice_index'][data], int(post_data['quantity']))
        self.assertEqual(len(bag), 1)
        self.assertRedirects(response, f'/products/{product.id}')

    def test_add_to_bag_product_unavailble(self):
        product = Product.objects.create(
            availability=False, name="Item",
            price=50, category_id=1, spice_index=True)
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        self.assertRedirects(response, '/')

    def test_add_to_bag_with_different_spice_index_product(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        post_data_two = {
            'quantity': '1',
            'spice_index': 'hot',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data_two)
        bag = self.client.session.get('bag', {})
        self.assertEqual(len(bag), 1)
        self.assertRedirects(response, f'/products/{product.id}')

    def test_add_to_bag_with_same_spice_index_product(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        post_data_two = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data_two)
        self.assertRedirects(response, f'/products/{product.id}')

    def test_add_to_bag_product_exists(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add 1st product
        post_data = {
            'quantity': '1',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        # Add same product again
        post_data_two = {
            'quantity': '1',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data_two)
        bag = self.client.session.get('bag', {})
        self.assertEqual(
            bag['1'], 2)
        self.assertEqual(len(bag), 1)
        self.assertRedirects(response, f'/products/{product.id}')

    """ Test Adjusting items in bag """
    def test_adjust_bag_no_spice_index(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        post_data = {
            'quantity': '1',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.Client.session
        post_data_two = {
            'quantity': '2',
        }
        response = self.client.post(reverse(
            'adjust_bag', args=[product.id]), data=post_data_two)
        bag2 = self.client.session.get('bag')
        self.assertEqual(bag2['1'], int(post_data_two['quantity']))
        self.assertRedirects(response, '/bag/')

    """ Test Adjusting items in bag """
    def test_adjust_bag_with_spice_index(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        post_data = {
            'quantity': '1',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.Client.session
        post_data_two = {
            'quantity': '2',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'adjust_bag', args=[product.id]), data=post_data_two)
        self.assertRedirects(response, '/bag/')

    """ Test deleting items from bag """
    def test_delete_from_bag_without_spice_index(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        post_data = {
            'quantity': '5',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        response = self.client.post(reverse(
            'delete_item', args=[product.id]))
        bag = self.client.session.get('bag')
        self.assertEqual(len(bag), 0)
        self.assertEqual(response.status_code, 200)

    """ Test deleting items from bag """
    def test_delete_from_bag_with_spice_index(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        post_data = {
            'quantity': '5',
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        post_data_two = {
            'spice_index': 'mild',
        }
        response = self.client.post(reverse(
            'delete_item', args=[product.id]), data=post_data_two)
        self.assertEqual(response.status_code, 200)

    def test_delete_from_bag_with_error(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        response = self.client.post(
                f'/bag/delete/{product.id}/', {'sss': 'mild'})
        self.assertEqual(response.status_code, 500)

    """ Check context view """
    # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.Response.context
    def test_bag_contents(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        # Add tester item to bag
        post_data = {
            'quantity': '6',
        }
        response = self.client.post(reverse(
            'add_to_bag', args=[product.id]), data=post_data)
        response = self.client.get('/bag/')
        self.assertEqual(response.context['grand_total'], 500)
        self.assertEqual(response.status_code, 200)

    def test_store_status(self):
        store_status = Store.objects.create(store_status='close')
        response = self.client.post('/bag/store_status/', {'status': 'open'})
        store_status = get_object_or_404(Store, id=1)
        response = self.client.get('/bag/')
        self.assertEqual(response.context['open_status'], True)
        self.assertEqual(store_status.store_status, 'open')
        self.assertEqual(response.status_code, 200)

    def test_store_status_close(self):
        response = self.client.post('/bag/store_status/', {'status': 'close'})
        response = self.client.get('/bag/')
        self.assertEqual(response.context['open_status'], False)

    def test_store_status_invalid(self):
        response = self.client.post('/bag/store_status/', {'sss': 'open'})
        self.assertEqual(response.status_code, 500)
