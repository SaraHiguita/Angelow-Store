from django.contrib import admin
from .models import Profile, Address, Wishlist

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'newsletter']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'is_default', 'address_type']
    list_filter = ['address_type', 'is_default', 'city']
    search_fields = ['user__username', 'street', 'city']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']