from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import random
# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a category (e.g. T-Shirt, Hoodie, etc.)')
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description = models.TextField(max_length=1000, help_text='Enter description of the product', null=True, blank=True)
    specification = models.TextField(max_length=1000, help_text='Enter specification of the product', null=True, blank=True)
    brand = models.CharField(max_length=200, help_text='Enter brand of the product', null=True, blank=True)
    color = models.CharField(max_length=200, help_text='Enter color of the product', null=True, blank=True)
    condition = models.CharField(max_length=200, help_text='Enter condition of the product', null=True, blank=True)
    image = models.ImageField(upload_to='images/product/', null=True, blank=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profile/', null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    nickname = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.User.username
    
class Expedition(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a expedition (e.g. JNE, TIKI, etc.)', null=True, blank=True)
    image = models.ImageField(upload_to='images/expedition/', null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Payment_method(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    tax = models.FloatField(default=0, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    order_number = models.CharField(max_length=10, unique=True, null=True, default=None)
    complete = models.BooleanField(default=False, null=True, blank=True)
    total_cost = models.FloatField(default=0, null=True, blank=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, null=True)
    payment_method = models.ForeignKey(Payment_method, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    
    @property
    def get_total_payment(self):
        total = self.get_cart_total() + self.expedition.price
        return total
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        order_number = str(random.randint(100000, 999999))
        return order_number

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self): 
        return str(self.id)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Shipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=200, null=False)
    province = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=200, null=True, blank=True)
    delivery_address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.delivery_address
