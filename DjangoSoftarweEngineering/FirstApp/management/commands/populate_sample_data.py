from django.core.management.base import BaseCommand
from FirstApp.models import Product, Customer, Order

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
        name='Game',
        price=19.20,
        available=True
        )
        customer1 = Customer.objects.create(
        name="Damian",
        address="NYC"
        )
        order1 = Order.objects.create(
        customer=customer1,
        status="NEW",
        date="2021-10-11"   

        )

        order1.products.add(product1)
        self.stdout.write("Data created successfully.")