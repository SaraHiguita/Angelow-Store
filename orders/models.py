from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('processing', 'En Proceso'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
        ('refunded', 'Reembolsado'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Número de Pedido')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Cliente')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado del Pedido')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name='Estado de Pago')
    
    # Direcciones
    shipping_address = models.TextField(verbose_name='Dirección de Envío')
    billing_address = models.TextField(verbose_name='Dirección de Facturación')
    
    # Totales - todos con default=0 para evitar None
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Subtotal')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Costo de Envío')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Impuestos')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Descuento')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total')
    
    # Información de pago
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Método de Pago')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='ID de Transacción')
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name='Número de Rastreo')
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Envío')
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Entrega')
    
    # Notas
    customer_notes = models.TextField(blank=True, verbose_name='Notas del Cliente')
    internal_notes = models.TextField(blank=True, verbose_name='Notas Internas')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido #{self.order_number}"
    
    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Generar número de pedido si no existe
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            last_id = last_order.id if last_order else 0
            self.order_number = f"ANG{10000 + last_id + 1}"
        
        # Asegurar que ningún campo sea None
        self.subtotal = self.subtotal or 0
        self.shipping_cost = self.shipping_cost or 0
        self.tax = self.tax or 0
        self.discount = self.discount or 0
        
        # Calcular total
        self.total = (self.subtotal + self.shipping_cost + self.tax) - self.discount
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    size = models.CharField(max_length=10, blank=True, verbose_name='Talla')
    color = models.CharField(max_length=50, blank=True, verbose_name='Color')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio Unitario')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio Total')
    
    class Meta:
        verbose_name = 'Item del Pedido'
        verbose_name_plural = 'Items del Pedido'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Asegurar valores por defecto
        self.unit_price = self.unit_price or 0
        self.quantity = self.quantity or 1
        
        # Calcular total
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Usuario')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
    
    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    def get_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        return total or 0
    
    def get_item_count(self):
        count = sum(item.quantity for item in self.items.all())
        return count or 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Carrito')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    size = models.CharField(max_length=10, blank=True, verbose_name='Talla')
    color = models.CharField(max_length=50, blank=True, verbose_name='Color')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ['cart', 'product', 'size', 'color']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def get_subtotal(self):
        price = self.product.get_final_price() if hasattr(self.product, 'get_final_price') else (self.product.discount_price or self.product.price)
        return (self.quantity or 0) * (price or 0)


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto Fijo'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, verbose_name='Tipo de Descuento')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor del Descuento')
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Compra Mínima')
    max_uses = models.PositiveIntegerField(default=0, verbose_name='Usos Máximos (0 = ilimitado)')
    used_count = models.PositiveIntegerField(default=0, verbose_name='Veces Usado')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    valid_from = models.DateTimeField(default=timezone.now, verbose_name='Válido Desde')
    valid_to = models.DateTimeField(verbose_name='Válido Hasta')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        return True

    def apply_discount(self, subtotal):
        if self.discount_type == 'percentage':
            return subtotal * (self.discount_value / 100)
        return min(self.discount_value, subtotal)


class Return(models.Model):
    REASON_CHOICES = [
        ('defective', 'Producto defectuoso'),
        ('wrong_item', 'Producto incorrecto'),
        ('size_issue', 'Problema de talla'),
        ('not_as_described', 'No coincide con la descripción'),
        ('changed_mind', 'Cambio de opinión'),
        ('other', 'Otro'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Solicitado'),
        ('approved', 'Aprobado'),
        ('received', 'Recibido'),
        ('refunded', 'Reembolsado'),
        ('rejected', 'Rechazado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns', verbose_name='Pedido')
    items = models.ManyToManyField(OrderItem, verbose_name='Artículos a Devolver')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name='Motivo')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested', verbose_name='Estado')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Monto a Reembolsar')
    admin_notes = models.TextField(blank=True, verbose_name='Notas del Administrador')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"Devolución #{self.id} - Pedido {self.order.order_number}"