from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BuilderSeller, Portfolio, Property, RentedSeller, RetailerSeller, User
from .forms import PropertyForm, LoginForm, UserRegisterForm
from .models import Property, Inquiry
from . import models  # Correct relative import
from django.db.models import Q  # Import Q for complex queries
# Function to render the home page
@login_required
def home(request):
    # Exclude properties owned by the logged-in user
    available_properties = Property.objects.exclude(owner=request.user)

    return render(request, 'users/home.html', {
        'properties': available_properties
    }) 

# Function to render the seller dashboard


# Function to filter properties
def filter_properties(request):
    properties = Property.objects.all()  # Retrieve all properties
    # Add filtering logic based on request parameters if needed
    return render(request, 'users/property_list.html', {'properties': properties})  # Assuming you have a property_list.html template

# Function to render inquiries

# Function to add a property to the cart
# Import for user feedback

# Function to render the investor's portfolio
def investor_portfolio(request):
    return render(request, 'users/investor_portfolio.html')  # Assuming you have an investor_portfolio.html template

# Function to search rentals
def search_rentals(request):
    query = request.GET.get('q')  # Get the search query from the request
    properties = Property.objects.filter(name__icontains=query)  # Filter properties based on the query
    return render(request, 'users/rental_list.html', {'properties': properties})  # Assuming you have a rental_list.html template

# Function to render the retailer's buyer page

# Function to render the user's profile page
def profile(request):
    return render(request, 'users/profile.html')  # Assuming you have a profile.html template

# Function to register a new user
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Function to handle user login
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

# Function to handle user logout
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

# Function to edit a property
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

# Function to list all properties
@login_required
def list_properties(request):
    # Exclude properties owned by the logged-in user
    available_properties = Property.objects.exclude(owner=request.user)

    return render(request, 'users/list_properties.html', {
        'properties': available_properties
    })
@login_required
def retailer_buyer(request):
    # Exclude properties owned by the logged-in user
    properties = Property.objects.filter(
        retailer_properties__isnull=False,
        status='Available'
    ).exclude(owner=request.user)

    return render(request, 'users/retailer_buyer.html', {'properties': properties})


@login_required
def investor_buyer(request):
    # Exclude properties owned by the logged-in user
    properties = Property.objects.filter(
        Q(retailer_properties__isnull=False) | Q(builder_properties__isnull=False),
        status='Available'
    ).exclude(owner=request.user).distinct()

    # Fetch the user's portfolio (example structure)
    portfolio_items = Portfolio.objects.filter(user=request.user)  # Assuming a Portfolio model exists

    return render(request, 'users/investor_buyer.html', {
        'properties': properties,
        'portfolio_items': portfolio_items,
    })


@login_required
def rented_buyer(request):
    # Filter properties available for rent and exclude properties owned by the logged-in user
    properties = Property.objects.filter(
        rented_properties__isnull=False,  # Ensure this field is correct for rented properties
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

    # Fetch properties listed by the RetailerSeller
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

    # Fetch properties listed by the BuilderSeller
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

    # Fetch properties listed by the RentedSeller
    rented_seller = RentedSeller.objects.filter(user=request.user).first()
    properties = rented_seller.properties.all() if rented_seller else []
    return render(request, 'users/rented_seller.html', {'form': form, 'properties': properties})


@login_required
def property_details(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'users/property_details.html', {'property': property})

def list_properties(request):
    properties = Property.objects.filter(is_sold=False)  # Only show unsold properties
    return render(request, 'users/property_list.html', {'properties': properties})

from .models import Property, Inquiry  # Assuming you have an Inquiry model

@login_required
def your_listings(request):
    # Fetch properties listed by the logged-in user
    properties = Property.objects.filter(owner=request.user)

    # Fetch inquiries related to the user's properties
    inquiries = Inquiry.objects.filter(property__owner=request.user)

    return render(request, 'users/your_listings.html', {
        'properties': properties,
        'inquiries': inquiries,
    })

from django.shortcuts import get_object_or_404, redirect
from .models import Cart

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

    return redirect('view_cart')  # Redirect to the cart page

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        message = request.POST.get('message')
        contact_info = request.POST.get('contact_info')

        # Validate and save the inquiry
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
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    except Cart.DoesNotExist:
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