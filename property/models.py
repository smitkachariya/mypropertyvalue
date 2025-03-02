from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=30)
    size = models.IntegerField()
    price = models.IntegerField()
    property_type = models.CharField(max_length=20)
    seller_type = models.CharField(max_length=20)
    image = models.ImageField(upload_to="property_images/")
    available = models.BooleanField()
    listed_by = models.CharField(max_length=30)

    def __str__(self):
        return f"Property: {self.title} in {self.location}"


class SaveProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"Saved Property: {self.property.title} by {self.user.username}"


status = [
    ('completed', 'Completed'),
    ('pending', 'Pending'),
    ('under_construction', 'Under Construction'),
]

class Builder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    building_status = models.CharField(max_length=50, choices=status)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Builder: {self.name} for {self.property.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    price_at_time_of_addition = models.DecimalField(max_digits=10, decimal_places=5)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart: {self.property.title} for {self.user.username}"


payment_method = [
    ('gpay', 'Google Pay'),
    ('phonepe', 'Phonepe'),
    ('upi', 'UPI'),
    ('cash', 'Cash'),
    ('card', 'Credit/Debit card'),
]

status = [
    ('completed', 'Completed'),
    ('pending', 'Pending'),
    ('failed', 'Failed'),
]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=30)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    price_sold = models.DecimalField(max_digits=10, decimal_places=5)
    transaction_status = models.CharField(max_length=20, choices=status)
    transaction_method = models.CharField(max_length=50, choices=payment_method)

    def __str__(self):
        return f"Transaction: {self.property.title} by {self.buyer_name}"


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=5)
    current_val = models.DecimalField(max_digits=10, decimal_places=5)
    ROI = models.FloatField()
    tenure = models.FloatField()

    def __str__(self):
        return f"Portfolio: {self.property.title} for {self.user.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField(max_length=100)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about {self.property.title}"


user_types = [
    ('retailer_buyer', 'Retailer_Buyer'),
    ('investor', 'Investor'),
    ('retailer_seller', 'Retailer_Seller'),
    ('builder', 'Builder'),
    ('rented', 'Rented'),
    ('admin', 'Admin'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30, choices=user_types)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"UserProfile: {self.user.username} - {self.user_type}"
