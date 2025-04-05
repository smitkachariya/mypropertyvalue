from django import views
from django.urls import path
from django.conf.urls.static import static

from mypropertyvalue import settings
from . import views
from .views import builder_seller, buyer_transactions, edit_property, home, register, login_view, logout_view, rented_seller, retailer_seller, seller_transactions, view_inquiries, filter_properties, add_to_cart, investor_portfolio, search_rentals, profile, list_properties, your_listings, your_transactions

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),

    path('', home, name='home'),

    path('rented-buyer/', views.rented_buyer, name='rented_buyer'),
    path('retailer-buyer/', views.retailer_buyer, name='retailer_buyer'),
    path('investor-buyer/', views.investor_buyer, name='investor_buyer'),

    path('add-to-cart/<int:property_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),

    path('property/<int:property_id>/', views.property_details, name='property_details'),
    path('properties/', list_properties, name='list_properties'), 
    path('properties/filter/', filter_properties, name='filter_properties'),

    
    path('property/buy/<int:property_id>/', views.buy_property, name='buy_property'),
    path('transactions/buyer/', buyer_transactions, name='buyer_transactions'),
    path('transactions/seller/', seller_transactions, name='seller_transactions'),
    path('transactions/', your_transactions, name='your_transactions'),

    path('retailer-seller/', retailer_seller, name='retailer_seller'),
    path('builder-seller/', builder_seller, name='builder_seller'),
    path('rented-seller/', rented_seller, name='rented_seller'),
   
    
   
    path("seller/edit/<int:property_id>/", edit_property, name="edit_property"),
    path("seller/inquiries/", view_inquiries, name="view_inquiries"),
    path('your-listings/', your_listings, name='your_listings'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
