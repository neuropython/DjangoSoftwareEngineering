from django.test import TestCase
from FirstApp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from decimal import Decimal

class ProductModelTest(TestCase):

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product',
        price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)
    
    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Temporary product',
            price=-2, available=True)
            temp_product.full_clean()
    
    def test_create_product_with_valid_data_2(self):
        temp_product = Product.objects.create(name='Dummy product',
        price=1000, available=False)
        self.assertEqual(temp_product.name, 'Dummy product')
        self.assertEqual(temp_product.price, 1000)
        self.assertFalse(temp_product.available)

    def test_create_product_with_invalid_name(self):
        temp_product = Product.objects.create(name='Temporary product',
        price=1.99, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

    def test_create_product_edge_name_value(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='A'*100, price=1.99, available=True)
            temp_product.full_clean()
            
    def test_create_product_edge_price_value(self):
        temp_product = Product.objects.create(name='Edge product',
        price=0.01, available=True)
        self.assertEqual(temp_product.name, 'Edge product')
        self.assertEqual(temp_product.price, 0.01)
        self.assertTrue(temp_product.available)
    
    def test_create_product_edge_price_value_2(self):
        temp_product = Product.objects.create(name='Edge product 2',
        price=1000000, available=True)
        self.assertEqual(temp_product.name, 'Edge product 2')
        self.assertEqual(temp_product.price, 1000000)
        self.assertTrue(temp_product.available)

class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer',
                                                address = 'Temporary address')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, 'Temporary address')
    
    def test_create_customer_with_invalid_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(address = 'Temporary address')
            temp_customer.full_clean()

    def test_create_customer_with_edge_name_value(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='A'*100,
            address = 'Temporary address')
            temp_customer.full_clean()

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Temporary customer',
                                                address = 'Temporary address')
        self.product1 = Product.objects.create(name='Temporary product 1',
                                                  price=1.99, available=True)  
         
    
    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, date='2022-02-02')
        temp_order.products.add(self.product1)
        self.assertEqual(temp_order.customer, self.customer)
        self.assertEqual(temp_order.date, '2022-02-02')
        self.assertEqual(temp_order.products.first(), self.product1)
        
    def test_create_order_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(date='2022-02-02', status = 'NOT_VALID', customer=self.customer)
            temp_order.products.add(self.product1)
            temp_order.full_clean()
    
    def test_calculate_total(self):
        temp_order = Order.objects.create(customer=self.customer, date='2022-02-02')
        temp_order.products.set([self.product1])
        self.assertEqual(temp_order.calculate_total(), Decimal('1.99'))
    
    def test_calculate_total_without_products(self):
        temp_order = Order.objects.create(customer=self.customer, date='2022-02-02')
        self.assertEqual(temp_order.calculate_total(), 0)
    
    def test_products_availability(self):
        temp_order = Order.objects.create(customer=self.customer, date='2022-02-02')
        temp_order.products.set([self.product1])
        self.assertTrue(temp_order.check_products_availability())
    
    def test_products_availability_with_unavailable_product(self):
        self.product1.available = False
        self.product1.save()
        temp_order = Order.objects.create(customer=self.customer, date='2022-02-02')
        temp_order.products.set([self.product1])
        self.assertFalse(temp_order.check_products_availability())
