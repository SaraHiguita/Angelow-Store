from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import shop_home, shop_product_list, shop_product_detail
from customers.views import role_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),

    # Redirect after login based on role
    path('redirect-after-login/', role_redirect, name='role_redirect'),

    # Auth URLs (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),

    # Tienda pública
    path('tienda/', shop_home, name='shop_home'),
    path('tienda/productos/', shop_product_list, name='shop_product_list'),
    path('tienda/productos/<slug:slug>/', shop_product_detail, name='shop_product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
