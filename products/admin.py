from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'created_at']
    list_filter = ['gender']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'stock_quantity', 'status', 'is_featured']
    list_filter = ['status', 'category', 'is_featured']  # ← Eliminado 'gender'
    list_editable = ['price', 'stock_quantity', 'status']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'sku', 'category', 'description')
        }),
        ('Precios y Stock', {
            'fields': ('price', 'discount_price', 'stock_quantity')
        }),
        ('Detalles', {
            'fields': ('sizes', 'colors', 'material', 'weight')
        }),
        ('Imagen y Estado', {
            'fields': ('main_image', 'status', 'is_featured')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'order']
    list_filter = ['product__category']