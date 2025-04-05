from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BuilderSeller, Portfolio, Property, Purchase, RentedSeller, RetailerSeller, User
from .forms import PropertyForm, LoginForm, UserRegisterForm
from .models import Property, Inquiry
from . import models  
from django.shortcuts import get_object_or_404, redirect
from .models import Cart

from django.utils.timezone import now

from .models import Transaction

@login_required
def home(request):
    
    available_properties = Property.objects.exclude(owner=request.user)

    return render(request, 'users/home.html', {
        'properties': available_properties
    }) 


def filter_properties(request):
    properties = Property.objects.all()  
    
    return render(request, 'users/property_list.html', {'properties': properties}) 

def investor_portfolio(request):
    return render(request, 'users/investor_portfolio.html')  

def search_rentals(request):
    query = request.GET.get('q')  
    properties = Property.objects.filter(name__icontains=query)  
    return render(request, 'users/rental_list.html', {'properties': properties})  

def profile(request):
    return render(request, 'users/profile.html') 

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') 


@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('your_listings')
    else:
        form = PropertyForm(instance=property)

    return render(request, 'users/edit_property.html', {'form': form, 'property': property})


@login_required
def list_properties(request):
    
    available_properties = Property.objects.exclude(owner=request.user)

    return render(request, 'users/list_properties.html', {
        'properties': available_properties
    })

@login_required
def retailer_buyer(request):
    
    properties = Property.objects.filter(
        retailer_properties__user__isnull=False,  
        status='Available'
    ).exclude(owner=request.user)

    return render(request, 'users/retailer_buyer.html', {'properties': properties})

@login_required
def investor_buyer(request):
    
    
    properties = Property.objects.filter(
        builder_properties__user__isnull=False, 
        status='Available'
    ).exclude(owner=request.user)

    return render(request, 'users/investor_buyer.html', {'properties': properties})
@login_required
def rented_buyer(request):
    
    properties = Property.objects.filter(
        rented_properties__user__isnull=False,  
        status='Available'
    ).exclude(owner=request.user)

    return render(request, 'users/rented_buyer.html', {'properties': properties})

@login_required
def retailer_seller(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            retailer_seller, created = RetailerSeller.objects.get_or_create(user=request.user)
            retailer_seller.properties.add(property)
            messages.success(request, 'Property listed successfully!')
            return redirect('retailer_seller')
    else:
        form = PropertyForm()

    
    retailer_seller = RetailerSeller.objects.filter(user=request.user).first()
    properties = retailer_seller.properties.all() if retailer_seller else []
    return render(request, 'users/retailer_seller.html', {'form': form, 'properties': properties})


@login_required
def builder_seller(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            builder_seller, created = BuilderSeller.objects.get_or_create(user=request.user)
            builder_seller.properties.add(property)
            messages.success(request, 'Property listed successfully!')
            return redirect('builder_seller')
    else:
        form = PropertyForm()

    builder_seller = BuilderSeller.objects.filter(user=request.user).first()
    properties = builder_seller.properties.all() if builder_seller else []
    return render(request, 'users/builder_seller.html', {'form': form, 'properties': properties})


@login_required
def rented_seller(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            rented_seller, created = RentedSeller.objects.get_or_create(user=request.user)
            rented_seller.properties.add(property)
            messages.success(request, 'Property listed successfully!')
            return redirect('rented_seller')
    else:
        form = PropertyForm()

    
    rented_seller = RentedSeller.objects.filter(user=request.user).first()
    properties = rented_seller.properties.all() if rented_seller else []
    return render(request, 'users/rented_seller.html', {'form': form, 'properties': properties})


@login_required
def property_details(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'users/property_details.html', {'property': property})

@login_required
def list_properties(request):
    properties = Property.objects.filter(is_sold=False)  
    return render(request, 'users/property_list.html', {'properties': properties})

from .models import Property, Inquiry  

@login_required
def your_listings(request):
    
    properties = Property.objects.filter(owner=request.user)

    inquiries = Inquiry.objects.filter(property__owner=request.user)

    return render(request, 'users/your_listings.html', {
        'properties': properties,
        'inquiries': inquiries,
    })



@login_required
def add_to_cart(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    buyer_type = request.GET.get('buyer_type', 'retailer_buyer')  # Default to 'retailer_buyer'

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        property=property,
        defaults={'buyer_type': buyer_type}
    )

    if created:
        messages.success(request, 'Property added to cart successfully!')
    else:
        messages.info(request, 'This property is already in your cart.')

    return redirect('view_cart')  

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        message = request.POST.get('message')
        contact_info = request.POST.get('contact_info')

        
        if property_id and message and contact_info:
            property = get_object_or_404(Property, id=property_id)
            Inquiry.objects.create(
                property=property,
                buyer=request.user,
                message=message,
                contact_info=contact_info
            )
            messages.success(request, 'Your inquiry has been sent successfully!')
            return redirect('view_cart')

    return render(request, 'users/cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        print(f"Deleting cart item: {cart_item}")
        cart_item.delete()
        print("Cart item deleted successfully.")
        messages.success(request, 'Item removed from cart successfully!')
    except Cart.DoesNotExist:
        print("Cart item not found.")
        messages.error(request, 'Cart item not found.')
    return redirect('view_cart')

@login_required
def view_inquiries(request):
    property_id = request.GET.get('property_id')
    if property_id:
        inquiries = Inquiry.objects.filter(property_id=property_id, property__owner=request.user)
    else:
        inquiries = Inquiry.objects.filter(property__owner=request.user)

    return render(request, 'users/view_inquiries.html', {'inquiries': inquiries})


@login_required
def buy_property(request, property_id):
    try:
       
        property = Property.objects.get(id=property_id, status='Available')
    except Property.DoesNotExist:
        messages.error(request, "The property you are trying to buy does not exist or is no longer available.")
        return redirect('view_cart')

    if property.owner == request.user:
        messages.error(request, "You cannot buy your own property.")
        return redirect('property_details', property_id=property_id)

    
    property.status = 'Sold'
    property.save()

    
    Transaction.objects.create(
        buyer=request.user,
        seller=property.owner,
        property=property
    )

    
    if hasattr(property.owner, 'retailerseller'):
        property.owner.retailerseller.properties.remove(property)
    if hasattr(property.owner, 'builderseller'):
        property.owner.builderseller.properties.remove(property)
    if hasattr(property.owner, 'rentedseller'):
        property.owner.rentedseller.properties.remove(property)

    
    Cart.objects.filter(user=request.user, property=property).delete()

    messages.success(request, "You have successfully purchased the property!")
    return redirect('your_transactions')  

@login_required
def seller_transactions(request):
    transactions = Transaction.objects.filter(seller=request.user).order_by('-transaction_date')
    return render(request, 'users/seller_transactions.html', {'transactions': transactions})

@login_required
def buyer_transactions(request):
    
    transactions = Transaction.objects.filter(buyer=request.user).order_by('-transaction_date')
    return render(request, 'users/buyer_transactions.html', {'transactions': transactions})
@login_required
def your_transactions(request):
    purchases = Transaction.objects.filter(buyer=request.user).order_by('-transaction_date')
    sales = Transaction.objects.filter(seller=request.user).order_by('-transaction_date')

    return render(request, 'users/your_transactions.html', {
        'purchases': purchases,
        'sales': sales,
    })