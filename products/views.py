from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Product, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
from customers.decorators import staff_required, StaffRequiredMixin


# ==================== TIENDA PÚBLICA ====================

def shop_home(request):
    products = Product.objects.filter(status='active').exclude(status='out_of_stock').select_related('category')[:12]
    categories = Category.objects.all()
    featured = Product.objects.filter(status='active', is_featured=True).exclude(status='out_of_stock').select_related('category')[:4]
    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'featured': featured,
    })


def shop_product_list(request):
    products = Product.objects.filter(status='active').exclude(status='out_of_stock').select_related('category')
    category_slug = request.GET.get('category')
    gender = request.GET.get('gender')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if gender:
        products = products.filter(category__gender=gender)
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/product_list.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    })


def shop_product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='active')
    related = Product.objects.filter(category=product.category, status='active').exclude(id=product.id)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
    })

# Dashboard Principal (Admin y Staff)
@staff_required
@login_required
def dashboard(request):
    from inventory.models import StockMovement, InventoryAlert
    from orders.models import Order
    from customers.models import Profile
    
    context = {
        'total_products': Product.objects.filter(status='active').count(),
        'low_stock_alerts': InventoryAlert.objects.filter(is_active=True).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'total_customers': Profile.objects.count(),
        'recent_products': Product.objects.order_by('-created_at')[:5],
        'recent_orders': Order.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)

# ==================== CATEGORÍAS ====================

class CategoryListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

class CategoryCreateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = "Categoría creada exitosamente."

class CategoryUpdateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = "Categoría actualizada exitosamente."

class CategoryDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'products/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Categoría eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

# ==================== PRODUCTOS ====================

class ProductListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['filters'] = {
            'category': self.request.GET.get('category', ''),
            'status': self.request.GET.get('status', ''),
            'search': self.request.GET.get('search', ''),
        }
        return context

class ProductDetailView(StaffRequiredMixin, LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class ProductCreateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')
    success_message = "Producto creado exitosamente."
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Procesar imágenes adicionales si se subieron
        images = self.request.FILES.getlist('additional_images')
        for i, image in enumerate(images):
            ProductImage.objects.create(
                product=self.object,
                image=image,
                order=i
            )
        return response

class ProductUpdateView(StaffRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    slug_url_kwarg = 'slug'
    success_message = "Producto actualizado exitosamente."
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Procesar imágenes adicionales
        images = self.request.FILES.getlist('additional_images')
        for i, image in enumerate(images):
            ProductImage.objects.create(
                product=self.object,
                image=image,
                order=ProductImage.objects.filter(product=self.object).count()
            )
        return response

class ProductDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

@staff_required
@login_required
def delete_product_image(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    product_slug = image.product.slug
    image.delete()
    messages.success(request, "Imagen eliminada exitosamente.")
    return redirect('product_detail', slug=product_slug)