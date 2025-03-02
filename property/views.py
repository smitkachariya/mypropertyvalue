from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Property
from .forms import PropertyForm

# ✅ 1️⃣ LIST VIEW (READ) - Show all properties
class PropertyListView(ListView):
    model = Property
    template_name = "property_list.html"
    context_object_name = "properties"

# ✅ 2️⃣ DETAIL VIEW (READ) - Show one property
class PropertyDetailView(DetailView):
    model = Property
    template_name = "property_detail.html"

# ✅ 3️⃣ CREATE VIEW - Add a new property
class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = "property_form.html"
    success_url = reverse_lazy("property_list")  # Redirect after success

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the logged-in user as the owner
        return super().form_valid(form)

# ✅ 4️⃣ UPDATE VIEW - Edit a property
class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = "property_form.html"
    success_url = reverse_lazy("property_list")

# ✅ 5️⃣ DELETE VIEW - Delete a property
class PropertyDeleteView(DeleteView):
    model = Property
    template_name = "property_confirm_delete.html"
    success_url = reverse_lazy("property_list")
