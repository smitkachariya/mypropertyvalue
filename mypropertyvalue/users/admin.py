from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cart, Inquiry, Transaction, User, Property, RetailerSeller, BuilderSeller, RentedSeller

admin.site.register(User, UserAdmin)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'property_type', 'location', 'get_is_sold')
    search_fields = ('title', 'location')
    list_filter = ('property_type', 'is_sold')

    def get_is_sold(self, obj):
        return obj.is_sold
    get_is_sold.boolean = True
    get_is_sold.short_description = 'Is Sold'

@admin.register(RetailerSeller)
class RetailerSellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_properties')

    def get_properties(self, obj):
        return ", ".join([property.title for property in obj.properties.all()])
    get_properties.short_description = 'Properties'

@admin.register(BuilderSeller)
class BuilderSellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_properties')

    def get_properties(self, obj):
        return ", ".join([property.title for property in obj.properties.all()])
    get_properties.short_description = 'Properties'

@admin.register(RentedSeller)
class RentedSellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_properties')

    def get_properties(self, obj):
        return ", ".join([property.title for property in obj.properties.all()])
    get_properties.short_description = 'Properties'

# Admin for Inquiry
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'contact_info', 'created_at')
    search_fields = ('property__title', 'buyer__username', 'contact_info')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'buyer_type', 'added_at')
    search_fields = ('user__username', 'property__title', 'buyer_type')
    list_filter = ('buyer_type', 'added_at')
    ordering = ('-added_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'seller', 'transaction_date')
    search_fields = ('property__title', 'buyer__username', 'seller__username')
    list_filter = ('transaction_date',)
    ordering = ('-transaction_date',)