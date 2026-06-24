from django.urls import path
from . import views

urlpatterns = [
    # Registro
    path('register/', views.register, name='register'),

    # Perfil
    path('profile/', views.profile_view, name='profile'),
    
    # Clientes
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    
    # Direcciones
    path('addresses/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('addresses/<int:pk>/update/', views.AddressUpdateView.as_view(), name='address_update'),
    path('addresses/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
    
    # Wishlist
    path('wishlist/add/<int:product_id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:pk>/', views.wishlist_remove, name='wishlist_remove'),
]