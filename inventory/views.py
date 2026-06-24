from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from .models import Supplier, StockMovement, InventoryAlert
from .forms import SupplierForm, StockMovementForm, InventoryAlertForm
from products.models import Product
from customers.decorators import staff_required, StaffRequiredMixin


@staff_required
@login_required
def inventory_dashboard(request):
    """Dashboard de inventario con estadísticas"""
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lte=10).count()
    total_inventory_value = Product.objects.aggregate(
        total=Sum(F('stock_quantity') * F('price'))
    )['total'] or 0
    
    recent_movements = StockMovement.objects.select_related('product', 'supplier').order_by('-created_at')[:10]
    active_alerts = InventoryAlert.objects.filter(is_active=True).select_related('product')
    
    context = {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'total_inventory_value': total_inventory_value,
        'recent_movements': recent_movements,
        'active_alerts': active_alerts,
    }
    return render(request, 'inventory/dashboard.html', context)


# ==================== PROVEEDORES ====================

class SupplierListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10


class SupplierCreateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')
    success_message = "Proveedor creado exitosamente."


class SupplierUpdateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')
    success_message = "Proveedor actualizado exitosamente."


class SupplierDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Proveedor eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# ==================== MOVIMIENTOS DE STOCK ====================

class StockMovementListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('product', 'supplier', 'created_by')
        
        movement_type = self.request.GET.get('type')
        product = self.request.GET.get('product')
        
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        if product:
            queryset = queryset.filter(product__name__icontains=product)
            
        return queryset


class StockMovementCreateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/movement_form.html'
    success_url = reverse_lazy('movement_list')
    success_message = "Movimiento registrado exitosamente."
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Validar stock antes de guardar para salidas
        if form.instance.movement_type == 'out':
            product = form.instance.product
            quantity = abs(form.instance.quantity)
            if product.stock_quantity < quantity:
                form.add_error('quantity', f'Stock insuficiente. Solo hay {product.stock_quantity} unidades disponibles.')
                return self.form_invalid(form)
        
        return super().form_valid(form)


# ==================== ALERTAS DE INVENTARIO ====================

class AlertListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = InventoryAlert
    template_name = 'inventory/alert_list.html'
    context_object_name = 'alerts'
    
    def get_queryset(self):
        return InventoryAlert.objects.select_related('product').filter(is_active=True)


class AlertCreateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = InventoryAlert
    form_class = InventoryAlertForm
    template_name = 'inventory/alert_form.html'
    success_url = reverse_lazy('alert_list')
    success_message = "Alerta creada exitosamente."


@staff_required
@login_required
def check_inventory_alerts(request):
    """Vista para verificar manualmente las alertas de inventario"""
    alerts = InventoryAlert.objects.filter(is_active=True)
    triggered = 0
    
    for alert in alerts:
        if alert.check_stock():
            triggered += 1
            alert.last_triggered = timezone.now()
            alert.save()
    
    if triggered > 0:
        messages.warning(request, f"¡Atención! {triggered} productos tienen stock bajo.")
    else:
        messages.success(request, "No hay alertas de inventario activas.")
    
    return redirect('inventory_dashboard')