from django.test import TestCase
from bag.models import Store
from products.models import Product, Category
from django.shortcuts import reverse


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

    """ Test Adjusting items in bag """
    def test_adjust_bag(self):
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

    """ Test deleting items from bag """
    def test_delete_from_bag(self):
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
