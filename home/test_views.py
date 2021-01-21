from django.test import TestCase
from bag.models import Store


# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')

    def test_view_bag(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
