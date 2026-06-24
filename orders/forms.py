from django import forms
from .models import Order, CartItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address', 'customer_notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Instrucciones especiales...'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'tracking_number', 'internal_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'size', 'color']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }