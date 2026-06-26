from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from .models import Order, OrderItem, Cart, CartItem, Coupon, Return
from .forms import OrderForm, OrderStatusForm, CartItemForm
from products.models import Product
from inventory.models import StockMovement
from customers.decorators import staff_required, StaffRequiredMixin

# ==================== CARRITO ====================

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart, 'cart_count': cart.get_item_count()})

@login_required
def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    size = request.POST.get('size', 'M')
    color = request.POST.get('color', 'Negro')
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f"'{product.name}' agregado al carrito.")

    if request.htmx:
        return render(request, 'partials/messages.html')
    return redirect('cart')

@login_required
def update_cart_item(request, pk):
    """Actualizar cantidad de item en carrito"""
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, "Cantidad actualizada.")
        else:
            item.delete()
            messages.success(request, "Producto eliminado del carrito.")

    if request.htmx:
        cart = item.cart if item.pk else Cart.objects.get_or_create(user=request.user)[0]
        return render(request, 'orders/cart.html', {'cart': cart})
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    """Eliminar item del carrito"""
    item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"'{product_name}' eliminado del carrito.")

    if request.htmx:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, 'orders/cart.html', {'cart': cart})
    return redirect('cart')

# ==================== ÓRDENES/PEDIDOS ====================

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 15

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Clientes solo ven sus pedidos; Staff/Admin ven todos
        if not (user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists()):
            queryset = queryset.filter(user=user)

        status = self.request.GET.get('status')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset.select_related('user').prefetch_related('items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_statuses'] = Order.STATUS_CHOICES
        user = self.request.user
        base_qs = Order.objects.all()
        if not (user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists()):
            base_qs = base_qs.filter(user=user)
        context['orders_count'] = base_qs.count()
        context['pending_count'] = base_qs.filter(status='pending').count()
        context['delivered_count'] = base_qs.filter(status='delivered').count()
        context['cancelled_count'] = base_qs.filter(status='cancelled').count()
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists():
            return super().get_queryset()
        return super().get_queryset().filter(user=user)

class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_message = "Pedido creado exitosamente."
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        cart = Cart.objects.filter(user=self.request.user).first()
        if cart:
            subtotal = cart.get_total()
            free_shipping_threshold = Decimal(str(getattr(settings, 'FREE_SHIPPING_THRESHOLD', '1000')))
            shipping_cost_value = Decimal(str(getattr(settings, 'SHIPPING_COST', '150')))
            tax_rate = Decimal(str(getattr(settings, 'TAX_RATE', '0.16')))

            form.instance.shipping_cost = shipping_cost_value if subtotal < free_shipping_threshold else 0
            form.instance.tax = subtotal * tax_rate
            form.instance.subtotal = subtotal
        
        response = super().form_valid(form)
        
        if cart:
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=self.object,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    size=cart_item.size,
                    color=cart_item.color,
                    unit_price=cart_item.product.get_final_price()
                )
            _reduce_stock(self.object)
            cart.items.all().delete()
        
        return response

class OrderUpdateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = 'orders/order_status_form.html'
    success_message = "Estado del pedido actualizado."
    
    def form_valid(self, form):
        # Si el estado cambia a 'shipped', registrar fecha
        if form.cleaned_data['status'] == 'shipped' and not self.object.shipped_at:
            form.instance.shipped_at = timezone.now()
        # Si cambia a 'delivered'
        if form.cleaned_data['status'] == 'delivered' and not self.object.delivered_at:
            form.instance.delivered_at = timezone.now()
            
        return super().form_valid(form)

def _reduce_stock(order):
    """Reduce stock y crea movimientos de inventario para cada item del pedido"""
    for item in order.items.all():
        available = item.product.stock_quantity
        qty = min(item.quantity, available) if available > 0 else 0
        if qty > 0:
            StockMovement.objects.create(
                product=item.product,
                movement_type='out',
                quantity=qty,
                notes=f"Venta - Pedido #{order.order_number}",
                reference_number=order.order_number,
            )


def _apply_coupon(subtotal, coupon_code):
    """Aplica cupón de descuento si es válido"""
    discount = 0
    coupon = None
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code.upper(), is_active=True)
            if not coupon.is_valid():
                return 0, None
            if subtotal < coupon.min_purchase:
                return 0, None
            discount = coupon.apply_discount(subtotal)
        except Coupon.DoesNotExist:
            pass
    return discount, coupon


@login_required
def create_order_from_cart(request):
    """Vista para crear orden desde el carrito"""
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('cart')

    if request.method == 'POST':
        subtotal = cart.get_total()
        free_shipping_threshold = Decimal(str(getattr(settings, 'FREE_SHIPPING_THRESHOLD', '1000')))
        shipping_cost_value = Decimal(str(getattr(settings, 'SHIPPING_COST', '150')))
        tax_rate = Decimal(str(getattr(settings, 'TAX_RATE', '0.16')))

        shipping = shipping_cost_value if subtotal < free_shipping_threshold else Decimal('0')
        tax = subtotal * tax_rate

        coupon_code = request.POST.get('coupon_code', '')
        discount, applied_coupon = _apply_coupon(subtotal, coupon_code)

        total = subtotal + shipping + tax - discount
        payment_method = request.POST.get('payment_method', 'mp')

        order = Order.objects.create(
            user=request.user,
            shipping_address=request.POST.get('shipping_address_final') or request.POST.get('shipping_address', ''),
            billing_address=request.POST.get('billing_address', ''),
            subtotal=subtotal,
            shipping_cost=shipping,
            tax=tax,
            discount=discount,
            total=total,
            customer_notes=request.POST.get('notes', ''),
            payment_method='Mercado Pago' if payment_method == 'mp' else 'Contra entrega',
            status='pending',
            payment_status='pending',
        )

        if applied_coupon:
            applied_coupon.used_count += 1
            applied_coupon.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                color=item.color,
                unit_price=item.product.get_final_price(),
            )

        _reduce_stock(order)
        cart.items.all().delete()

        # Enviar email de confirmación
        if order.user.email:
            try:
                subject = f"Pedido #{order.order_number} confirmado - ANGELOW"
                html_message = render_to_string('emails/order_confirmation.html', {'order': order})
                send_mail(
                    subject,
                    f"Gracias por tu compra. Pedido #{order.order_number} confirmado.",
                    settings.DEFAULT_FROM_EMAIL,
                    [order.user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception:
                pass

        if payment_method == 'mp':
            from .mercadopago_utils import create_payment_preference
            preference = create_payment_preference(order, request)
            if preference and 'init_point' in preference:
                return redirect(preference['init_point'])

        messages.success(request, f"¡Pedido #{order.order_number} creado exitosamente!")
        return redirect('order_detail', pk=order.pk)

    addresses = request.user.addresses.all()
    coupon_code = request.GET.get('coupon', '')
    discount = 0
    if coupon_code:
        discount, _ = _apply_coupon(cart.get_total(), coupon_code)
        if discount > 0:
            messages.success(request, f"¡Cupón aplicado! Descuento: ${discount:.2f}")
        else:
            messages.error(request, "Cupón inválido o vencido.")

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'discount': discount,
        'coupon_code': coupon_code,
        'mercadopago_public_key': __import__('decouple').config('MERCADO_PAGO_PUBLIC_KEY', default=''),
    })


# ==================== CANCELACIÓN POR CLIENTE ====================

@login_required
def cancel_order(request, pk):
    """Permite al cliente cancelar un pedido pendiente"""
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status != 'pending':
        messages.error(request, "Solo puedes cancelar pedidos pendientes.")
        return redirect('order_detail', pk=order.pk)

    if request.method == 'POST':
        order.status = 'cancelled'
        order.payment_status = 'refunded'
        order.save()

        # Restaurar stock
        for item in order.items.all():
            StockMovement.objects.create(
                product=item.product,
                movement_type='return',
                quantity=item.quantity,
                notes=f"Cancelación - Pedido #{order.order_number}",
                reference_number=order.order_number,
            )

        messages.success(request, f"Pedido #{order.order_number} cancelado exitosamente.")
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/cancel_confirm.html', {'order': order})


# ==================== DEVOLUCIONES / REEMBOLSOS ====================

class ReturnCreateView(LoginRequiredMixin, CreateView):
    model = Return
    fields = ['reason', 'description']
    template_name = 'orders/return_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=kwargs['order_pk'], user=request.user)
        if self.order.status not in ['delivered', 'shipped']:
            messages.error(request, "Solo puedes solicitar devolución de pedidos entregados o enviados.")
            return redirect('order_detail', pk=self.order.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order
        form.instance.status = 'requested'
        response = super().form_valid(form)
        form.instance.items.set(self.order.items.all())
        messages.success(self.request, "Solicitud de devolución creada. Te contactaremos pronto.")
        return response

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context


class ReturnListView(LoginRequiredMixin, ListView):
    model = Return
    template_name = 'orders/return_list.html'
    context_object_name = 'returns'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists():
            return Return.objects.select_related('order').all()
        return Return.objects.filter(order__user=user).select_related('order')


class ReturnDetailView(LoginRequiredMixin, DetailView):
    model = Return
    template_name = 'orders/return_detail.html'
    context_object_name = 'return_obj'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists():
            return Return.objects.select_related('order')
        return Return.objects.filter(order__user=user).select_related('order')


@staff_required
@login_required
def update_return_status(request, pk):
    """Actualizar estado de una devolución (Staff/Admin)"""
    return_obj = get_object_or_404(Return, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        refund_amount = request.POST.get('refund_amount')
        admin_notes = request.POST.get('admin_notes', '')

        return_obj.status = new_status
        return_obj.admin_notes = admin_notes
        if refund_amount:
            return_obj.refund_amount = refund_amount
        return_obj.save()

        if new_status == 'refunded':
            return_obj.order.payment_status = 'refunded'
            return_obj.order.status = 'refunded'
            return_obj.order.save()

        messages.success(request, f"Devolución #{return_obj.id} actualizada a '{return_obj.get_status_display()}'.")
        return redirect('return_detail', pk=return_obj.pk)

    return render(request, 'orders/return_status_form.html', {'return_obj': return_obj})


# ==================== MERCADO PAGO ====================

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json


def mp_create_preference(request, order_id):
    """Crea una preferencia de pago en Mercado Pago"""
    from .mercadopago_utils import create_payment_preference
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    preference = create_payment_preference(order, request)
    if preference and 'id' in preference:
        return JsonResponse({'preference_id': preference['id'], 'init_point': preference.get('init_point', '')})
    return JsonResponse({'error': 'Error al crear la preferencia de pago'}, status=500)


def mp_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment_id = request.GET.get('payment_id')
    if payment_id:
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.transaction_id = payment_id
        order.payment_method = 'Mercado Pago'
        order.save()
        messages.success(request, f'¡Pago exitoso! Pedido #{order.order_number} confirmado.')
    return redirect('order_detail', pk=order.pk)


def mp_failure(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    messages.error(request, 'El pago no pudo ser procesado. Intenta de nuevo.')
    return redirect('checkout')


def mp_pending(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    messages.warning(request, 'Tu pago está pendiente de confirmación.')
    return redirect('order_detail', pk=order.pk)


@csrf_exempt
def mp_webhook(request):
    """Webhook para recibir notificaciones de Mercado Pago"""
    if request.method == 'POST':
        from .mercadopago_utils import handle_mp_webhook
        try:
            data = json.loads(request.body)
            handle_mp_webhook(data)
            return HttpResponse(status=200)
        except (json.JSONDecodeError, Exception):
            return HttpResponse(status=400)
    return HttpResponse(status=405)