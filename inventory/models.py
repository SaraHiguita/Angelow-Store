from django.db import models
from django.urls import reverse
from products.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Persona de Contacto')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    address = models.TextField(blank=True, verbose_name='Dirección')
    tax_id = models.CharField(max_length=50, blank=True, verbose_name='RFC/NIT')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
        ('return', 'Devolución'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements', verbose_name='Producto')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name='Tipo de Movimiento')
    quantity = models.IntegerField(verbose_name='Cantidad')
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Costo Unitario')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Costo Total')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Proveedor')
    reference_number = models.CharField(max_length=100, blank=True, verbose_name='Número de Referencia')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Calcular costo total
        if self.unit_cost and self.quantity:
            self.total_cost = abs(self.quantity) * self.unit_cost
        
        # Validar stock antes de guardar
        if self.movement_type == 'out':
            if self.product.stock_quantity < abs(self.quantity):
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Stock insuficiente. Solo hay {self.product.stock_quantity} unidades disponibles.")
        
        super().save(*args, **kwargs)
        
        # Actualizar stock del producto
        if self.movement_type == 'in':
            self.product.stock_quantity += abs(self.quantity)
        elif self.movement_type == 'out':
            self.product.stock_quantity -= abs(self.quantity)
        elif self.movement_type == 'return':
            self.product.stock_quantity += abs(self.quantity)
        elif self.movement_type == 'adjustment':
            self.product.stock_quantity = abs(self.quantity)
        
        self.product.save()


class InventoryAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts', verbose_name='Producto')
    threshold = models.PositiveIntegerField(default=10, verbose_name='Umbral Mínimo')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    last_triggered = models.DateTimeField(blank=True, null=True, verbose_name='Última Alerta')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Alerta de Inventario'
        verbose_name_plural = 'Alertas de Inventario'
    
    def __str__(self):
        return f"Alerta: {self.product.name} (min: {self.threshold})"
    
    def check_stock(self):
        if self.product.stock_quantity <= self.threshold:
            return True
        return False