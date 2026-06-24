from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    GENDER_CHOICES = [
        ('M', 'Hombre'),
        ('F', 'Mujer'),
        ('U', 'Unisex'),
        ('K', 'Niños'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    description = models.TextField(blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Imagen')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2XL'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('out_of_stock', 'Sin Stock'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True, verbose_name='SKU')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Precio de Oferta')
    main_image = models.ImageField(upload_to='products/main/', verbose_name='Imagen Principal')
    sizes = models.CharField(max_length=200, default='S,M,L', verbose_name='Tallas Disponibles (separadas por coma)')
    colors = models.CharField(max_length=200, default='Negro,Blanco', verbose_name='Colores (separados por coma)')
    material = models.CharField(max_length=100, blank=True, verbose_name='Material')
    stock_quantity = models.IntegerField(default=0, verbose_name='Cantidad en Stock')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
    is_featured = models.BooleanField(default=False, verbose_name='Destacado')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Peso (kg)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    def get_sizes_list(self):
        return [s.strip() for s in self.sizes.split(',')]
    
    def get_colors_list(self):
        return [c.strip() for c in self.colors.split(',')]
    
    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    def get_final_price(self):
        return self.discount_price if self.is_on_sale() else self.price
    
    def clean(self):
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'El stock no puede ser negativo.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Producto')
    image = models.ImageField(upload_to='products/gallery/', verbose_name='Imagen')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Texto Alternativo')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')
    
    class Meta:
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
        ordering = ['order']
    
    def __str__(self):
        return f"Imagen de {self.product.name}"