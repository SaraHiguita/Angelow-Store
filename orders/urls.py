from django.urls import path
from . import views

urlpatterns = [
    # Carrito
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout
    path('checkout/', views.create_order_from_cart, name='checkout'),

    # Órdenes
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel_order'),

    # Devoluciones
    path('returns/', views.ReturnListView.as_view(), name='return_list'),
    path('returns/<int:pk>/', views.ReturnDetailView.as_view(), name='return_detail'),
    path('returns/<int:pk>/update-status/', views.update_return_status, name='update_return_status'),
    path('orders/<int:order_pk>/return/', views.ReturnCreateView.as_view(), name='return_create'),

    # Mercado Pago
    path('mp-create-preference/<int:order_id>/', views.mp_create_preference, name='mp_create_preference'),
    path('mp-success/<int:order_id>/', views.mp_success, name='mp_success'),
    path('mp-failure/<int:order_id>/', views.mp_failure, name='mp_failure'),
    path('mp-pending/<int:order_id>/', views.mp_pending, name='mp_pending'),
    path('mp-webhook/', views.mp_webhook, name='mp_webhook'),
]