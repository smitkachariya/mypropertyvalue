from django import views
from django.urls import path
from . import views
from .views import home, register, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
      path('retailer-buyer/', views.retailer_buyer, name='retailer_buyer'),
    path('investor-buyer/', views.investor_buyer, name='investor_buyer'),
    path('sellers/', views.seller_page, name='seller_page'),
]
