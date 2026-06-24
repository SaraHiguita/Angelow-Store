from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Coupon, Return

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'user__username', 'user__email', 'tracking_number']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'total']
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Direcciones', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Totales', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')
        }),
        ('Pago y Envío', {
            'fields': ('payment_method', 'transaction_id', 'tracking_number', 'shipped_at', 'delivered_at')
        }),
        ('Notas', {
            'fields': ('customer_notes', 'internal_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'get_total', 'get_item_count']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'size', 'color']
    list_filter = ['size', 'color']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code']

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'reason', 'status', 'refund_amount', 'created_at']
    list_filter = ['status', 'reason']
    search_fields = ['order__order_number']