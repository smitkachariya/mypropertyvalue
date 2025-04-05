import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class Property(models.Model):
    PROPERTY_TYPES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Unnamed Property") # New status field
    is_sold = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')  # Add this field

    
    
    def __str__(self):
        return self.title

class Buyer(models.Model):
    BUYER_TYPE_CHOICES = [
        ('Retailer', 'Retailer'),
        ('Investor', 'Investor'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES)
    interested_properties = models.ManyToManyField(Property, blank=True)


class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    contact_info = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.buyer.username} for {self.property.title}"
    

class RetailerSeller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, related_name='retailer_properties')

    def __str__(self):
        return self.user.username

class BuilderSeller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, related_name='builder_properties')

    def __str__(self):
        return self.user.username

class RentedSeller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, related_name='rented_properties')

    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    BUYER_TYPE_CHOICES = [
        ('retailer_buyer', 'Retailer Buyer'),
        ('investor_buyer', 'Investor Buyer'),
        ('rented_buyer', 'Rented Buyer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES, default='retailer_buyer')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.property.title} ({self.get_buyer_type_display()})"
    
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    roi = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Return on Investment
    tenure = models.IntegerField(default=0)  # Tenure in years

#     def __str__(self):
#         return f"{self.user.username} - {self.property.title}"
    

class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_sales')
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.property.title} from {self.seller.username}"
    
class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_sales')
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.property.title} from {self.seller.username}"