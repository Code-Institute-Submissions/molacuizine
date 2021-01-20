from django.test import TestCase


# Create your tests here.
class TestBagViews(TestCase):

    def test_view_bag(self):
        response = self.client.get('/bag/')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
