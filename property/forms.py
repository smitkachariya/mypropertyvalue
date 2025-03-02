from django import forms
from .models import Property, SaveProperty, Builder, Cart, Transaction, Portfolio, Notification, UserProfile

# Property Form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'size', 'price', 'property_type', 'seller_type', 'image', 'available', 'listed_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

# Save Property Form
class SavePropertyForm(forms.ModelForm):
    class Meta:
        model = SaveProperty
        fields = ['property']

# Builder Form
class BuilderForm(forms.ModelForm):
    class Meta:
        model = Builder
        fields = ['property', 'name', 'location', 'building_status', 'contact_number']

# Cart Form
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['property', 'price_at_time_of_addition', 'quantity']

# Transaction Form
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['buyer_name', 'property', 'transaction_date', 'price_sold', 'transaction_status', 'transaction_method']

# Portfolio Form
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['property', 'purchase_price', 'current_val', 'ROI', 'tenure']

# Notification Form
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['property', 'message', 'is_read']

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type', 'phone_number']
