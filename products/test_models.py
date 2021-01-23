from django.test import TestCase
from .models import Product, Category


class TestProductModels(TestCase):

    def setUp(self):
        self.Category = Category.objects.create(
            id=1, name="sides", friendly_name='Sides')

    def test_item_string_returns_names(self):

        product = Product.objects.create(
            name='item', price=2000, category_id=1)
        self.assertAlmostEqual(str(product), 'item')
