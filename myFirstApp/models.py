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