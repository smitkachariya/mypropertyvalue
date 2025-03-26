from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import login, logout

from .models import Property, Buyer, Seller

# Home Page
def home(request):
    properties = Property.objects.all()
    return render(request, 'users/home.html', {'properties': properties})

# Retailer Buyer Page
def retailer_buyer(request):
    retailer_properties = Property.objects.filter(property_type='Residential')
    return render(request, 'users/retailer_buyer.html', {'properties': retailer_properties})

# Investor Page
def investor_buyer(request):
    investor_properties = Property.objects.filter(property_type='Commercial')
    return render(request, 'users/investor_buyer.html', {'properties': investor_properties})

# Seller Page (Excluding rented sellers)
def seller_page(request):
    sellers = Seller.objects.exclude(seller_type='Rented Seller')
    return render(request, 'users/seller.html', {'sellers': sellers})
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after register
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout
