from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    
    # Proveedores
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Movimientos
    path('movements/', views.StockMovementListView.as_view(), name='movement_list'),
    path('movements/create/', views.StockMovementCreateView.as_view(), name='movement_create'),
    
    # Alertas
    path('alerts/', views.AlertListView.as_view(), name='alert_list'),
    path('alerts/create/', views.AlertCreateView.as_view(), name='alert_create'),
    path('alerts/check/', views.check_inventory_alerts, name='check_alerts'),
]