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
        self.assertRedirects(response, f'/products/{product.id}')

    """ Test Adjusting items in bag """
    def test_adjust_bag(self):
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        post_data = {
            'quantity': '1',
        }
        response = self.client.post(reverse(
            'adjust_bag', args=[product.id]), data=post_data)

        self.assertRedirects(response, '/bag/')
