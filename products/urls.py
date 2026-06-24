from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Categorías
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Productos
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Imágenes
    path('product-images/<int:pk>/delete/', views.delete_product_image, name='delete_product_image'),
]