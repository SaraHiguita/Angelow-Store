from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Product, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'gender', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-url-amigable'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        return name


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    additional_images = MultipleFileField(
        required=False,
        label="Imágenes adicionales",
        help_text="Puedes seleccionar múltiples imágenes manteniendo presionada la tecla Ctrl"
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'sku', 'category', 'description',
            'price', 'discount_price', 'main_image', 'sizes',
            'colors', 'material', 'stock_quantity', 'weight',
            'status', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ANG-001'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sizes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'S, M, L, XL'}),
            'colors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Negro, Blanco, Azul'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Algodón, Poliéster, etc.'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        return price

    def clean_discount_price(self):
        price = self.cleaned_data.get('price')
        discount = self.cleaned_data.get('discount_price')
        if discount is not None and price and discount >= price:
            raise ValidationError('El precio de oferta debe ser menor al precio original.')
        if discount is not None and discount <= 0:
            raise ValidationError('El precio de oferta debe ser mayor a 0.')
        return discount

    def clean_stock_quantity(self):
        qty = self.cleaned_data.get('stock_quantity')
        if qty is not None and qty < 0:
            raise ValidationError('El stock no puede ser negativo.')
        return qty

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            raise ValidationError('El SKU es obligatorio.')
        if Product.objects.filter(sku=sku).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este SKU ya está en uso.')
        return sku


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_order(self):
        order = self.cleaned_data.get('order')
        if order is not None and order < 0:
            raise ValidationError('El orden no puede ser negativo.')
        return order
