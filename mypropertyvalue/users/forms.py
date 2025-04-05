from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Property
from django import forms
from .models import Inquiry
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'location', 'price', 'description', 'image', 'property_type','status']


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message', 'contact_info']