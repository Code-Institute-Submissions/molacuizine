from django.test import TestCase
from django.test import Client
from bag.models import Store

c = Client()
url = '/bag/'
r = c.get(url)
print(r)
print(r.status_code)
print(r.status_code)

# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')

    def test_view_bag(self):
        response = self.client.get('/')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
