from django.test import TestCase
from bag.models import Store
from django.shortcuts import reverse, get_object_or_404
from products.models import Product, Category
from django.contrib.auth.models import User


# Create your tests here.
class ProductTestViews(TestCase):

    def setUp(self):
        self.Store = Store.objects.create(store_status='open')
        self.Category = Category.objects.create(
            id=1, name="sides", friendly_name='Sides')
        self.product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)

    def test_all_product_page(self):
        response = self.client.get('/products/', {'page_number': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_search_with_no_q_query(self):
        response = self.client.get(reverse('query_search'), {'q': ''})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

    def test_product_search_with__q_query_and_no_page_number(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        response = self.client.get(reverse('query_search'), {'q': 'rice'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/query_search.html')

    def test_product_search_with__q_query_and_page_number(self):
        response = self.client.get(reverse(
            'query_search'), {'q': 'rice', 'page_number': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/query_search.html')

    def test_product_search_with_category_no_page_number(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        response = self.client.get(
            reverse('category_search'), {'category': 'sides'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_search.html')

    def test_product_search_with_category_and_page_number(self):
        response = self.client.get(
            reverse('category_search'),
            {'category': 'sides', 'page_number': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_search.html')

    def test_store_management_page_no_super_user(self):
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        response = self.client.get(reverse('store_management'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_store_management_page_with_super_user(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        response = self.client.get(reverse('store_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/store_management.html')

    def test_add_product_page_with_valid_post(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        data = {
            'name': 'item',
            'description': 'An item',
            'price': 50,
            'category': 1,
            'spice_index': True,
        }
        response = self.client.post(reverse('store_management'), data)
        product = get_object_or_404(Product, id=2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/products/{product.id}')

    def test_add_product_page_with_invalid_post(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        data = {
            'name': 'item',
            'description': 'An item',
            'price': 50,
            'category': 'xxxx',
            'spice_index': True,
        }
        response = self.client.post(reverse('store_management'), data)
        self.assertEqual(response.status_code, 302)

    def test_product_update_no_super_user(self):
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        response = self.client.get(
            f'/products/product_update/{self.product.id}')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_product_update_with_super_user(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        response = self.client.get(
            f'/products/product_update/{self.product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_update.html')

    def test_update_product_page_with_valid_post(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        data = {
            'name': 'item',
            'description': 'An item',
            'price': 50,
            'category': 1,
            'spice_index': True,
        }
        response = self.client.post(
            f'/products/product_update/{self.product.id}', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/products/{self.product.id}')

    def test_update_product_page_with_invalid_post(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        data = {
            'name': 'item',
            'description': 'An item',
            'price': 50,
            'category': 'xxx',
            'spice_index': True,
        }
        response = self.client.post(
            f'/products/product_update/{self.product.id}', data)
        self.assertEqual(response.status_code, 302)

    def test_product_delete_no_super_user(self):
        self.user = User.objects.create_user(
            username='testuser', password='zahur')
        self.client.login(
            username='testuser', password='zahur')
        response = self.client.get(
            f'/products/product_delete/{self.product.id}')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_product_delete_with_super_user(self):
        self.user = User.objects.create_superuser(
            username='superuser', password='zahur')
        self.client.login(
            username='superuser', password='zahur')
        response = self.client.get(
            f'/products/product_delete/{self.product.id}')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')
