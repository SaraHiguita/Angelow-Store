from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Address


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este correo ya está registrado.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'avatar', 'preferences', 'newsletter']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+52 555 123 4567'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tus estilos preferidos...'}),
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.replace('+', '').replace(' ', '').replace('-', '').isdigit():
            raise ValidationError('Ingresa un número de teléfono válido.')
        return phone


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'name', 'street', 'city', 'state', 'zip_code', 'country', 'phone', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Casa, Oficina'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle y número'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code or len(zip_code) < 3:
            raise ValidationError('Ingresa un código postal válido.')
        return zip_code
