from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
# Property Model
class Property(models.Model):
    PROPERTY_TYPES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

# Buyer Model (Retailer & Investor)
class Buyer(models.Model):
    BUYER_TYPE_CHOICES = [
        ('Retailer', 'Retailer'),
        ('Investor', 'Investor'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES)
    interested_properties = models.ManyToManyField(Property, blank=True)

# Seller Model
class Seller(models.Model):
    SELLER_TYPE_CHOICES = [
        ('Home Owner', 'Home Owner'),
        ('Developer', 'Developer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES)
    properties = models.ManyToManyField(Property)
