from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Foto de Perfil')
    preferences = models.TextField(blank=True, verbose_name='Preferencias de Estilo')
    newsletter = models.BooleanField(default=True, verbose_name='Suscrito al Newsletter')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"

class Address(models.Model):
    ADDRESS_TYPES = [
        ('shipping', 'Envío'),
        ('billing', 'Facturación'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='Usuario')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='shipping', verbose_name='Tipo')
    name = models.CharField(max_length=100, verbose_name='Nombre de la Dirección (ej: Casa, Oficina)')
    street = models.CharField(max_length=200, verbose_name='Calle y Número')
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    state = models.CharField(max_length=100, verbose_name='Estado/Provincia')
    zip_code = models.CharField(max_length=20, verbose_name='Código Postal')
    country = models.CharField(max_length=100, default='México', verbose_name='País')
    is_default = models.BooleanField(default=False, verbose_name='Dirección Principal')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono de Contacto')
    
    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'
        ordering = ['-is_default', '-id']
    
    def __str__(self):
        return f"{self.name} - {self.street}, {self.city}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Desmarcar otras direcciones por defecto del mismo tipo
            Address.objects.filter(user=self.user, address_type=self.address_type).update(is_default=False)
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name='Usuario')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Producto')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Agregado el')
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"