from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import login, logout

from .models import Inquiry, Property, Buyer, Seller

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
def seller_dashboard(request):
    if request.method == "POST":
        seller_type = request.POST.get("seller_type")

        if seller_type == "retailer":
            title = request.POST.get("title")
            location = request.POST.get("location")
            estimated_price = get_estimated_price(location)  # Function to fetch price
            manual_price = request.POST.get("manual_price")
            description = request.POST.get("description")

            property_obj = Property.objects.create(
                title=title,
                location=location,
                estimated_price=manual_price or estimated_price,
                description=description,
                seller_type="retailer"
            )
            property_obj.save()

        elif seller_type == "builder":
            project_name = request.POST.get("project_name")
            location = request.POST.get("location")
            price_range = request.POST.get("price_range")
            status = request.POST.get("status")
            description = request.POST.get("description")

            property_obj = Property.objects.create(
                title=project_name,
                location=location,
                price_range=price_range,
                status=status,
                description=description,
                seller_type="builder"
            )
            property_obj.save()

        return redirect("seller_dashboard")

    properties = Property.objects.all()
    return render(request, "users/seller.html", {"properties": properties})


def get_estimated_price(location):
    recent_properties = Property.objects.filter(location=location).order_by("-id")[:3]
    if recent_properties.exists():
        avg_price = sum([prop.estimated_price for prop in recent_properties]) / len(recent_properties)
        return f"₹{avg_price}"
    return "No matching properties found. Enter price manually."

def edit_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    if request.method == "POST":
        property_obj.title = request.POST.get("title")
        property_obj.location = request.POST.get("location")
        property_obj.price_range = request.POST.get("price_range")
        property_obj.description = request.POST.get("description")
        property_obj.save()
        return redirect("seller_dashboard")
    
    return render(request, "users/edit_property.html", {"property": property_obj})

def view_inquiries(request):
    inquiries = Inquiry.objects.all()
    return render(request, "users/inquiries.html", {"inquiries": inquiries})
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
