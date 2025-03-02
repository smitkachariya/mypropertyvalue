from django.urls import path
from .views import (
    PropertyListView, PropertyDetailView, 
    PropertyCreateView, PropertyUpdateView, PropertyDeleteView
)

urlpatterns = [
    path("", PropertyListView.as_view(), name="property_list"),  # Show all properties
    path("property/<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),  # Show one property
    path("property/new/", PropertyCreateView.as_view(), name="property_create"),  # Add new property
    path("property/<int:pk>/edit/", PropertyUpdateView.as_view(), name="property_update"),  # Edit property
    path("property/<int:pk>/delete/", PropertyDeleteView.as_view(), name="property_delete"),  # Delete property
]
