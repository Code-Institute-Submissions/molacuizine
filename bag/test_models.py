from django.test import TestCase
from bag.models import Store


class TestModels(TestCase):

    def test_store_status(self):
        store = Store.objects.create(store_status='open')
        self.assertEqual(store.store_status, 'open')

    def test_item_string_returns_name(self):
        store = Store.objects.create(store_status='open')
        self.assertAlmostEqual(str(store), 'open')
