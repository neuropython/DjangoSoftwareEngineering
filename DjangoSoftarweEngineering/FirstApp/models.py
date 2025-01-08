from django.db import models
from django.core.exceptions import ValidationError



class Product(models.Model):

    def price_validator(value):
        if value < 0:
            raise ValidationError('Price must be greater than 0')   
        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Ensure max_length is set to 50
    price = models.DecimalField(max_digits=10, decimal_places=2,  validators=[price_validator])
    available = models.BooleanField()


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)


class Order(models.Model):

    def calculate_total(self):
        total = 0
        for product in self.products.all():
            total += product.price
        return total
    
    def check_products_availability(self):
        for product in self.products.all():
            if not product.available:
                return False
        return True
    
            
    
            

    id = models.AutoField(primary_key=True)
    products =models.ManyToManyField(Product)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
     

    class OrderType(models.TextChoices):
        NEW = 'NEW', 'New'
        IN_PROCESS = 'IN_PROCESS', 'In Process'
        SENT = 'SENT', 'Sent'
        COMPLETED = 'COMPLETED', 'Completed'

    status =  models.CharField(
        choices=OrderType.choices
        )
