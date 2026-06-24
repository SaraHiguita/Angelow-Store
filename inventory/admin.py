from django.contrib import admin
from .models import Supplier, StockMovement, InventoryAlert

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_person', 'email']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'created_at', 'created_by']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'reference_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(InventoryAlert)
class InventoryAlertAdmin(admin.ModelAdmin):
    list_display = ['product', 'threshold', 'is_active', 'last_triggered']
    list_filter = ['is_active']