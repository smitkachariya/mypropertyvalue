from django import views
from django.urls import path
from . import views
from .views import edit_property, home, register, login_view, logout_view, seller_dashboard, view_inquiries

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
      path('retailer-buyer/', views.retailer_buyer, name='retailer_buyer'),
    path('investor-buyer/', views.investor_buyer, name='investor_buyer'),
      path('seller/', seller_dashboard, name='seller_dashboard'),
    path("seller/edit/<int:property_id>/", edit_property, name="edit_property"),
    path("seller/inquiries/", view_inquiries, name="view_inquiries"),
]
