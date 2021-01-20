from django.test import TestCase
from django.test import Client
c = Client()

# Create your tests here.
class TestViews(TestCase):

    def test_view_bag(self):
        response = self.client.get('/bag')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
