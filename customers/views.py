from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.db import models
from django.utils import timezone
from .models import Profile, Address, Wishlist
from .forms import ProfileForm, AddressForm, UserForm
from .decorators import staff_required, StaffRequiredMixin


def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect('shop_home')
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard')
    if request.user.groups.filter(name='Staff').exists():
        return redirect('inventory_dashboard')
    return redirect('shop_home')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    from orders.models import Cart
    Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'addresses': request.user.addresses.all(),
        'wishlist': request.user.wishlist.select_related('product')[:10],
    }
    return render(request, 'customers/profile.html', context)


# ==================== CLIENTES (USUARIOS) ====================

class CustomerListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False).select_related('profile')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search)
            )
        return queryset.order_by('-date_joined')


class CustomerDetailView(StaffRequiredMixin, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.order_by('-created_at')[:10]
        context['addresses'] = self.object.addresses.all()
        context['wishlist'] = self.object.wishlist.select_related('product')
        return context


# ==================== DIRECCIONES ====================

class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'customers/address_form.html'
    success_message = "Dirección agregada exitosamente."
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile')


class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'customers/address_form.html'
    success_message = "Dirección actualizada exitosamente."
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('profile')


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'customers/address_confirm_delete.html'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, "Dirección eliminada exitosamente.")
        return reverse_lazy('profile')


# ==================== WISHLIST ====================

@login_required
def wishlist_add(request, product_id):
    """Agregar producto a wishlist"""
    from products.models import Product
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, f"'{product.name}' agregado a tu lista de deseos.")
    else:
        messages.info(request, f"'{product.name}' ya está en tu lista de deseos.")

    if request.htmx:
        return render(request, 'partials/messages.html')
    return redirect('shop_product_detail', slug=product.slug)


@login_required
def wishlist_remove(request, pk):
    """Eliminar producto de wishlist"""
    item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"'{product_name}' eliminado de tu lista de deseos.")
    return redirect('profile')


# ==================== REGISTRO ====================

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        errors = {}
        if not username:
            errors['username'] = 'El nombre de usuario es obligatorio.'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'El nombre de usuario ya existe.'
        if not email:
            errors['email'] = 'El correo electrónico es obligatorio.'
        if not password1 or len(password1) < 8:
            errors['password1'] = 'La contraseña debe tener al menos 8 caracteres.'
        if password1 != password2:
            errors['password2'] = 'Las contraseñas no coinciden.'

        if not errors:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            Profile.objects.get_or_create(user=user)
            from orders.models import Cart
            Cart.objects.get_or_create(user=user)
            cliente_group = Group.objects.get(name='Cliente')
            user.groups.add(cliente_group)
            user = authenticate(request, username=username, password=password1)
            if user:
                login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a ANGELOW.')
            return redirect('shop_home')

        for field, error in errors.items():
            messages.error(request, error)

    return render(request, 'registration/register.html')