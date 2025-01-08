from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from FirstApp.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class BaseProductApiTest(APITestCase):
    
    def setUp(self):
        self.product = Product.objects.create(name='Temporary Product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.client = APIClient()

    def authenticate_user(self, user):
        token = str(AccessToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class ProductApiTestNormalUser(BaseProductApiTest):
    
    def setUp(self):
        super().setUp()
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.authenticate_user(self.regular_user)

    def test_get_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_a_single_product(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary Product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_create_a_product(self):
        data = {'name': 'New Product', 'price': 2.99, 'available': True}
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_a_product(self):
        data = {'name': 'Updated Product', 'price': 3.99, 'available': False}
        response = self.client.put(self.product_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductApiTestAdmin(BaseProductApiTest):
    
    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')
        self.authenticate_user(self.admin)

    def test_get_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_a_single_product(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary Product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_create_a_product(self):
        data = {'name': 'New Product', 'price': 2.99, 'available': True}
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='New Product').price, Decimal('2.99'))
        self.assertTrue(Product.objects.get(name='New Product').available)

    def test_update_a_product(self):
        data = {'name': 'Updated Product', 'price': 3.99, 'available': False}
        response = self.client.put(self.product_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get(name='Updated Product').price, Decimal('3.99'))
        self.assertFalse(Product.objects.get(name='Updated Product').available)

    def test_delete_a_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
