# Documentación del Proyecto ANGELOW Store

**ANGELOW** es una plataforma de comercio electrónico para una marca de moda premium, construida con Django 6.0. Este sistema permite la gestión completa de productos, inventario, clientes, pedidos y pagos en línea.

---

## Tabla de Contenidos

1. [Tecnologías Utilizadas](#1-tecnologías-utilizadas)
2. [Arquitectura del Proyecto](#2-arquitectura-del-proyecto)
3. [Modelos y Base de Datos](#3-modelos-y-base-de-datos)
4. [Validaciones](#4-validaciones)
5. [Capas de Seguridad](#5-capas-de-seguridad)
6. [Funcionalidades del Proyecto](#6-funcionalidades-del-proyecto)
7. [Instalación y Configuración](#7-instalación-y-configuración)
8. [Pruebas](#8-pruebas)

---

## 1. Tecnologías Utilizadas

### Backend
| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.13 | Lenguaje de programación |
| Django | 6.0.3 | Framework web principal |
| SQLite | 3.x | Base de datos (desarrollo) |
| WhiteNoise | 6.12.0 | Servir archivos estáticos en producción |
| Gunicorn/uWSGI | — | Servidor WSGI (producción) |

### Frontend
| Tecnología | Versión | Propósito |
|---|---|---|
| Bootstrap 5 | 5.3.0 | Framework CSS (diseño responsive) |
| HTMX | 2.0.4 | Interacciones AJAX sin JavaScript |
| Alpine.js | 3.14.8 | Estado interactivo en el cliente |
| Bootstrap Icons | 1.10.0 | Iconografía |

### Procesamiento de Formularios
| Tecnología | Propósito |
|---|---|
| django-crispy-forms 2.6 | Renderizado elegante de formularios |
| crispy-bootstrap5 2026.3 | Template pack Bootstrap 5 para crispy |

### Pagos
| Tecnología | Propósito |
|---|---|
| mercadopago 3.2.0 | SDK oficial de Mercado Pago |

### Seguridad
| Tecnología | Propósito |
|---|---|
| django-csp 4.0 | Content Security Policy |
| django-ratelimit 4.1.0 | Rate limiting en login |

### Testing
| Tecnología | Propósito |
|---|---|
| pytest 9.1.1 | Framework de pruebas |
| pytest-django 4.12.0 | Plugin Django para pytest |
| httpx 0.28.1 | Cliente HTTP para pruebas |

### Otros
| Tecnología | Propósito |
|---|---|
| Pillow 12.1.1 | Procesamiento de imágenes |
| python-decouple 3.8 | Gestión de variables de entorno |
| django-htmx 1.27.0 | Integración Django + HTMX |

---

## 2. Arquitectura del Proyecto

### Estructura de Directorios

```
angelow-store/
├── angelow/                  # Configuración del proyecto Django
│   ├── settings.py           # Configuración general
│   ├── urls.py               # Enrutamiento raíz
│   ├── wsgi.py               # WSGI entry point
│   └── asgi.py               # ASGI entry point
│
├── products/                 # App: Gestión de productos y categorías
├── inventory/                # App: Gestión de inventario y proveedores
├── customers/                # App: Usuarios, perfiles, direcciones, wishlist
├── orders/                   # App: Carrito, checkout, pedidos, cupones, devoluciones
│
├── templates/                # Plantillas HTML (46 archivos)
│   ├── base.html             # Plantilla base con navbar, footer, Alpine, HTMX
│   ├── shop/                 # Tienda pública (home, listado, detalle)
│   ├── products/             # CRUD de productos y categorías (admin)
│   ├── orders/               # Carrito, checkout, pedidos, devoluciones
│   ├── customers/            # Perfil, direcciones, listado clientes
│   ├── inventory/            # Dashboard inventario, proveedores, movimientos
│   ├── registration/         # Login, registro, recuperación password
│   ├── partials/             # Fragmentos HTML reutilizables
│   └── emails/               # Plantillas de correo electrónico
│
├── static/                   # Archivos estáticos fuente
│   ├── css/style.css         # Estilos personalizados (tema lujo)
│   ├── js/main.js            # JavaScript personalizado
│   └── images/               # Imágenes del sitio
│
├── media/                    # Archivos subidos por usuarios
├── staticfiles/              # Estáticos recolectados (producción)
├── manage.py                 # Script de gestión Django
├── requirements.txt          # Dependencias Python
├── pytest.ini                # Configuración de pytest
└── .env                      # Variables de entorno
```

### Patrón Arquitectónico

El proyecto sigue el patrón **MVT (Model-View-Template)** de Django con una arquitectura de **aplicaciones modulares**. Cada app encapsula una funcionalidad de negocio específica:

- **products**: Catálogo de productos y categorías
- **orders**: Flujo completo de ventas (carrito → checkout → pago → pedido)
- **customers**: Gestión de usuarios, autenticación y perfiles
- **inventory**: Control de stock, proveedores y alertas

### Flujo de Navegación

```
Usuario no autenticado:
  Tienda pública → Registro/Login → Carrito → Checkout → Pago MP → Pedido

Usuario Cliente:
  Tienda → Carrito → Checkout → Pago → Mis Pedidos → Devolución

Usuario Staff/Admin:
  Dashboard → Productos/Categorías → Inventario → Clientes → Pedidos → Devoluciones
```

---

## 3. Modelos y Base de Datos

### Diagrama de Relaciones

```
Category (Categoría)
  └── Product (Producto)
        ├── ProductImage (Imágenes de Producto)
        ├── CartItem (Item en Carrito) ── Cart (Carrito) ── User
        ├── OrderItem (Item en Pedido) ── Order (Pedido) ── User
        │     └── Return (Devolución)
        ├── StockMovement (Movimiento de Stock) ── Supplier (Proveedor)
        └── InventoryAlert (Alerta de Inventario)

User (Usuario Django)
  ├── Profile (Perfil)
  ├── Address (Dirección)
  └── Wishlist (Lista de Deseos) ── Product

Coupon (Cupón de Descuento) [independiente]
```

### Modelos Detallados

#### products/models.py

**Category** (`products_category`)
| Campo | Tipo | Detalles |
|---|---|---|
| name | CharField(100) | Nombre de la categoría |
| slug | SlugField | Único, para URLs |
| gender | CharField(1) | Choices: M=Hombre, F=Mujer, U=Unisex, K=Niños |
| description | TextField | Opcional |
| image | ImageField | Subida a `categories/` |
| created_at | DateTimeField | Auto, solo creación |

**Product** (`products_product`)
| Campo | Tipo | Detalles |
|---|---|---|
| name | CharField(200) | Nombre del producto |
| slug | SlugField | Único |
| sku | CharField(50) | Único, ej: ANG-001 |
| category | ForeignKey(Category) | Relación con categoría |
| description | TextField | Descripción detallada |
| price | DecimalField(10,2) | Precio original |
| discount_price | DecimalField(10,2) | Precio con descuento (nullable) |
| main_image | ImageField | Imagen principal |
| sizes | CharField(200) | Tallas separadas por coma |
| colors | CharField(200) | Colores separados por coma |
| material | CharField(100) | Material del producto |
| stock_quantity | IntegerField | Stock actual |
| status | CharField(20) | Choices: active, inactive, out_of_stock |
| is_featured | BooleanField | Destacado en tienda |
| weight | DecimalField(5,2) | Peso en kg (nullable) |
| created_at | DateTimeField | Auto creación |
| updated_at | DateTimeField | Auto actualización |

**ProductImage** (`products_productimage`)
| Campo | Tipo | Detalles |
|---|---|---|
| product | ForeignKey(Product) | Relación con producto |
| image | ImageField | Subida a `products/gallery/` |
| alt_text | CharField(200) | Texto alternativo |
| order | PositiveIntegerField | Orden de visualización |

#### customers/models.py

**Profile** (`customers_profile`)
| Campo | Tipo | Detalles |
|---|---|---|
| user | OneToOneField(User) | Relación 1:1 con usuario Django |
| phone | CharField(20) | Teléfono |
| birth_date | DateField | Fecha de nacimiento |
| avatar | ImageField | Foto de perfil |
| preferences | TextField | Preferencias de estilo |
| newsletter | BooleanField | Suscripción a newsletter |

**Address** (`customers_address`)
| Campo | Tipo | Detalles |
|---|---|---|
| user | ForeignKey(User) | Dueño de la dirección |
| address_type | CharField(20) | shipping o billing |
| name | CharField(100) | Ej: Casa, Oficina |
| street | CharField(200) | Calle y número |
| city | CharField(100) | Ciudad |
| state | CharField(100) | Estado/Provincia |
| zip_code | CharField(20) | Código postal |
| country | CharField(100) | Default: México |
| is_default | BooleanField | Dirección principal |
| phone | CharField(20) | Teléfono de contacto |

**Wishlist** (`customers_wishlist`)
| Campo | Tipo | Detalles |
|---|---|---|
| user | ForeignKey(User) | Dueño |
| product | ForeignKey(Product) | Producto deseado |
| added_at | DateTimeField | Fecha de adición |
| notes | TextField | Notas personales |

**Unique together:** (user, product)

#### orders/models.py

**Order** (`orders_order`)
| Campo | Tipo | Detalles |
|---|---|---|
| order_number | CharField(20) | Único, formato: ANG1xxxx |
| user | ForeignKey(User) | Cliente |
| status | CharField(20) | pending, confirmed, processing, shipped, delivered, cancelled, refunded |
| payment_status | CharField(20) | pending, paid, failed, refunded |
| shipping_address | TextField | Dirección de envío |
| billing_address | TextField | Dirección de facturación |
| subtotal | DecimalField(10,2) | Default 0 |
| shipping_cost | DecimalField(10,2) | Default 0 |
| tax | DecimalField(10,2) | Default 0 |
| discount | DecimalField(10,2) | Default 0 |
| total | DecimalField(10,2) | Calculado automáticamente |
| payment_method | CharField(50) | Método de pago |
| transaction_id | CharField(100) | ID de transacción |
| tracking_number | CharField(100) | Número de rastreo |
| shipped_at | DateTimeField | Fecha de envío |
| delivered_at | DateTimeField | Fecha de entrega |
| customer_notes | TextField | Notas del cliente |
| internal_notes | TextField | Notas internas (staff) |

**OrderItem** (`orders_orderitem`)
| Campo | Tipo | Detalles |
|---|---|---|
| order | ForeignKey(Order) | Pedido padre |
| product | ForeignKey(Product) | Producto |
| quantity | PositiveIntegerField | Cantidad |
| size | CharField(10) | Talla seleccionada |
| color | CharField(50) | Color seleccionado |
| unit_price | DecimalField(10,2) | Precio unitario al momento de la compra |
| total_price | DecimalField(10,2) | Calculado: quantity × unit_price |

**Cart** (`orders_cart`)
| Campo | Tipo | Detalles |
|---|---|---|
| user | OneToOneField(User) | Dueño del carrito |

**CartItem** (`orders_cartitem`)
| Campo | Tipo | Detalles |
|---|---|---|
| cart | ForeignKey(Cart) | Carrito padre |
| product | ForeignKey(Product) | Producto |
| quantity | PositiveIntegerField | Cantidad |
| size | CharField(10) | Talla |
| color | CharField(50) | Color |

**Unique together:** (cart, product, size, color)

**Coupon** (`orders_coupon`)
| Campo | Tipo | Detalles |
|---|---|---|
| code | CharField(50) | Único, código del cupón |
| discount_type | CharField(20) | percentage o fixed |
| discount_value | DecimalField(10,2) | Valor del descuento |
| min_purchase | DecimalField(10,2) | Compra mínima para aplicar |
| max_uses | PositiveIntegerField | 0 = ilimitado |
| used_count | PositiveIntegerField | Veces usado |
| is_active | BooleanField | Activo/inactivo |
| valid_from | DateTimeField | Inicio de vigencia |
| valid_to | DateTimeField | Fin de vigencia |

**Return** (`orders_return`)
| Campo | Tipo | Detalles |
|---|---|---|
| order | ForeignKey(Order) | Pedido a devolver |
| items | ManyToManyField(OrderItem) | Artículos a devolver |
| reason | CharField(20) | defective, wrong_item, size_issue, not_as_described, changed_mind, other |
| description | TextField | Descripción detallada |
| status | CharField(20) | requested, approved, received, refunded, rejected |
| refund_amount | DecimalField(10,2) | Monto a reembolsar |
| admin_notes | TextField | Notas del administrador |

#### inventory/models.py

**Supplier** (`inventory_supplier`)
| Campo | Tipo | Detalles |
|---|---|---|
| name | CharField(200) | Nombre del proveedor |
| contact_person | CharField(100) | Persona de contacto |
| email | EmailField | Correo electrónico |
| phone | CharField(20) | Teléfono |
| address | TextField | Dirección |
| tax_id | CharField(50) | RFC/NIT |
| is_active | BooleanField | Activo |

**StockMovement** (`inventory_stockmovement`)
| Campo | Tipo | Detalles |
|---|---|---|
| product | ForeignKey(Product) | Producto |
| movement_type | CharField(20) | in, out, adjustment, return |
| quantity | IntegerField | Cantidad (positiva o negativa) |
| unit_cost | DecimalField(10,2) | Costo unitario |
| total_cost | DecimalField(10,2) | Calculado: abs(qty) × unit_cost |
| supplier | ForeignKey(Supplier) | Proveedor (nullable) |
| reference_number | CharField(100) | Número de referencia |
| notes | TextField | Notas |
| created_by | ForeignKey(User) | Usuario que registró |

**InventoryAlert** (`inventory_inventoryalert`)
| Campo | Tipo | Detalles |
|---|---|---|
| product | ForeignKey(Product) | Producto a monitorear |
| threshold | PositiveIntegerField | Default 10, umbral mínimo |
| is_active | BooleanField | Alerta activa |
| last_triggered | DateTimeField | Última vez que se disparó |

---

## 4. Validaciones

### 4.1 Validaciones a Nivel de Modelo (Model.clean)

**Product** (`products/models.py:90-92`)
- `stock_quantity`: No puede ser negativo
  ```python
  def clean(self):
      if self.stock_quantity < 0:
          raise ValidationError({'stock_quantity': 'El stock no puede ser negativo.'})
  ```

**StockMovement** (`inventory/models.py:52-75`)
- **Salidas (out)**: Verifica stock suficiente antes de registrar
  ```python
  if self.movement_type == 'out':
      if self.product.stock_quantity < abs(self.quantity):
          raise ValidationError(...)
  ```
- **Actualización automática de stock**: Al guardar, suma/resta la cantidad al producto relacionado según el tipo de movimiento

**Address** (`customers/models.py:46-50`)
- **Dirección principal**: Solo una dirección por tipo puede ser default
  ```python
  if self.is_default:
      Address.objects.filter(user=self.user, address_type=self.address_type).update(is_default=False)
  ```

**Order** (`orders/models.py:69-85`)
- **Generación automática de order_number**: Formato `ANG1xxxx`
- **Cálculo automático del total**: `subtotal + shipping_cost + tax - discount`

**OrderItem** (`orders/models.py:104-111`)
- **Cálculo automático**: `total_price = quantity × unit_price`

### 4.2 Validaciones a Nivel de Formulario (Form.clean)

#### products/forms.py

**CategoryForm**
| Campo | Validación |
|---|---|
| `name` | Mínimo 3 caracteres |

**ProductForm**
| Campo | Validación |
|---|---|
| `price` | Debe ser mayor a 0 |
| `discount_price` | Debe ser menor al precio original y mayor a 0 |
| `stock_quantity` | No puede ser negativo |
| `sku` | Obligatorio, único en base de datos |

**ProductImageForm**
| Campo | Validación |
|---|---|
| `order` | No puede ser negativo |

#### customers/forms.py

**UserForm**
| Campo | Validación |
|---|---|
| `email` | Único en base de datos (excluyendo el usuario actual) |

**ProfileForm**
| Campo | Validación |
|---|---|
| `phone` | Debe contener solo dígitos, espacios, + y - |

**AddressForm**
| Campo | Validación |
|---|---|
| `zip_code` | Mínimo 3 caracteres |

#### inventory/forms.py

**SupplierForm**
| Campo | Validación |
|---|---|
| `name` | Mínimo 3 caracteres |

**StockMovementForm**
| Campo | Validación |
|---|---|
| `quantity` | No puede ser 0 |
| `unit_cost` | No puede ser negativo |

**InventoryAlertForm**
| Campo | Validación |
|---|---|
| `threshold` | Entre 0 y 99999 |

### 4.3 Validaciones a Nivel de Vista

| Vista | Validación |
|---|---|
| `register()` | Username obligatorio y único, email obligatorio, password ≥ 8 caracteres, passwords coinciden |
| `cancel_order()` | Solo pedidos en estado "pending" pueden cancelarse |
| `ReturnCreateView.dispatch()` | Solo pedidos "delivered" o "shipped" pueden tener devolución |
| `create_order_from_cart()` | Verifica que el carrito no esté vacío |
| `StockMovementCreateView.form_valid()` | Verifica stock suficiente para movimientos tipo "out" |
| `update_cart_item()` | Si cantidad ≤ 0, elimina el item del carrito |

### 4.4 Validaciones en la Base de Datos

- **unique=True**: slug (Category, Product), sku (Product), order_number (Order), code (Coupon)
- **unique_together**: (user, product) en Wishlist; (cart, product, size, color) en CartItem
- **blank=True**, **null=True**: Campos opcionales
- **default=**: Valores por defecto para evitar None

---

## 5. Capas de Seguridad

### 5.1 Autenticación de Usuarios

Django Authentication System con los siguientes validadores de contraseña (`settings.py:71-76`):

1. `UserAttributeSimilarityValidator` — Evita contraseñas similares a atributos del usuario
2. `MinimumLengthValidator` — Longitud mínima de contraseña
3. `CommonPasswordValidator` — Evita contraseñas comunes
4. `NumericPasswordValidator` — Evita contraseñas numéricas

### 5.2 Autorización por Roles (RBAC)

Tres grupos de usuarios creados automáticamente mediante señal `post_migrate` (`customers/signals.py`):

| Grupo | Permisos | Acceso |
|---|---|---|
| **Admin** | Superusuario — todos los permisos | Dashboard completo, todo el sistema |
| **Staff** | CRUD selectivo: Categorías, Productos, Imágenes, Pedidos, Items, Carritos, Proveedores, Movimientos, Alertas, Perfiles, Direcciones, Cupones, Devoluciones + ver Usuarios | Panel administrativo, inventario, clientes |
| **Cliente** | Sin permisos especiales | Tienda pública, perfil propio, pedidos propios |

**Decoradores y Mixins** (`customers/decorators.py`):

| Decorador/Mixin | Función |
|---|---|
| `@staff_required` | Redirige si el usuario no es Staff/Admin |
| `@admin_required` | Redirige si el usuario no es Admin |
| `StaffRequiredMixin` | Para CBV, lanza PermissionDenied si no es Staff |
| `AdminRequiredMixin` | Para CBV, lanza PermissionDenied si no es Admin |

**Uso en vistas**:
```python
@staff_required
@login_required
def dashboard(request):
    ...

class ProductListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    ...
```

### 5.3 Separación Cliente vs Staff

En vistas de listado/detalle de pedidos y devoluciones, se filtra según el rol:
- **Clientes**: Solo ven sus propios registros
- **Staff/Admin**: Ven todos los registros

```python
# orders/views.py:100-101
if not (user.is_superuser or user.groups.filter(name__in=['Admin', 'Staff']).exists()):
    queryset = queryset.filter(user=user)
```

### 5.4 Protección CSRF

- Middleware CSRF activo (`CsrfViewMiddleware`)
- CSRF cookie: `HttpOnly=True`, `SameSite='Lax'`
- `@csrf_exempt` solo en el webhook de Mercado Pago (ruta externa)

### 5.5 Seguridad en Sesiones

| Configuración (`settings.py`) | Valor |
|---|---|
| `SESSION_COOKIE_AGE` | 86400 segundos (24 horas) |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | True |
| `SESSION_COOKIE_HTTPONLY` | True |
| `SESSION_COOKIE_SAMESITE` | 'Lax' |
| `CSRF_COOKIE_HTTPONLY` | True |
| `CSRF_COOKIE_SAMESITE` | 'Lax' |

### 5.6 Seguridad en Producción

Cuando `DEBUG = False`:

| Configuración | Valor |
|---|---|
| `SECURE_SSL_REDIRECT` | True |
| `SECURE_HSTS_SECONDS` | 31536000 (1 año) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | True |
| `SECURE_HSTS_PRELOAD` | True |
| `SESSION_COOKIE_SECURE` | True |
| `CSRF_COOKIE_SECURE` | True |
| `SECURE_PROXY_SSL_HEADER` | ('HTTP_X_FORWARDED_PROTO', 'https') |

### 5.7 Rate Limiting

- `django-ratelimit` configurado para la vista de login (solo en producción)
- Previene ataques de fuerza bruta en el formulario de inicio de sesión

### 5.8 Content Security Policy (CSP)

- `django-csp` instalado para mitigar ataques XSS
- Controla qué recursos (scripts, estilos, fuentes) puede cargar el navegador

### 5.9 WhiteNoise Security

- `CompressedManifestStaticFilesStorage` para servir archivos estáticos
- Headers de caché automáticos para archivos estáticos

### 5.10 Otras Medidas de Seguridad

| Medida | Implementación |
|---|---|
| **Redirección post-login** | `role_redirect` según grupo de usuario |
| **Manejo de errores** | Mensajes de error genéricos (no revelan existencia de usuarios) |
| **Protección de rutas** | Decoradores `@login_required` en todas las rutas sensibles |
| **Validación de propiedad** | `get_object_or_404(CartItem, pk=pk, cart__user=request.user)` |
| **UUID/Longitud en order_number** | Formato predecible pero no secuencial simple |
| **HTTPS en webhooks** | URLs absolutas con `request.build_absolute_uri()` |

---

## 6. Funcionalidades del Proyecto

### 6.1 Tienda Pública

| Ruta | Vista | Descripción |
|---|---|---|
| `/tienda/` | `shop_home` | Página principal con productos activos, categorías y destacados |
| `/tienda/productos/` | `shop_product_list` | Listado con filtros (categoría, género, búsqueda, rango de precio), paginación (12) |
| `/tienda/productos/<slug>/` | `shop_product_detail` | Detalle con galería de imágenes, selector de talla/color, add-to-cart |

### 6.2 Dashboard Principal

| Ruta | Vista | Descripción |
|---|---|---|
| `/` | `dashboard` | Estadísticas: total productos, alertas de stock, pedidos pendientes, clientes registrados, productos y pedidos recientes |

**Requiere:** Staff/Admin

### 6.3 Gestión de Categorías (CRUD)

| Ruta | Vista | Descripción |
|---|---|---|
| `/categories/` | `CategoryListView` | Listado con paginación |
| `/categories/create/` | `CategoryCreateView` | Crear categoría |
| `/categories/<slug>/update/` | `CategoryUpdateView` | Editar categoría |
| `/categories/<slug>/delete/` | `CategoryDeleteView` | Eliminar categoría |

### 6.4 Gestión de Productos (CRUD)

| Ruta | Vista | Descripción |
|---|---|---|
| `/products/` | `ProductListView` | Listado con filtros (categoría, estado, búsqueda) |
| `/products/<slug>/` | `ProductDetailView` | Detalle completo del producto |
| `/products/create/` | `ProductCreateView` | Crear producto + imágenes adicionales múltiples |
| `/products/<slug>/update/` | `ProductUpdateView` | Editar producto + imágenes adicionales |
| `/products/<slug>/delete/` | `ProductDeleteView` | Eliminar producto |
| `/product-images/<pk>/delete/` | `delete_product_image` | Eliminar imagen individual |

### 6.5 Carrito de Compras

| Ruta | Vista | Descripción |
|---|---|---|
| `/orders/cart/` | `cart_view` | Ver carrito, cantidades, subtotales |
| `/orders/cart/add/<product_id>/` | `add_to_cart` | Agregar producto con talla/color (HTMX) |
| `/orders/cart/update/<pk>/` | `update_cart_item` | Actualizar cantidad (HTMX) |
| `/orders/cart/remove/<pk>/` | `remove_from_cart` | Eliminar item (HTMX) |

**Características:**
- Contador de carrito en navbar con Alpine.js
- Actualizaciones vía HTMX (sin recarga)
- Sincronización automática del badge del carrito

### 6.6 Checkout y Pedidos

| Ruta | Vista | Descripción |
|---|---|---|
| `/orders/checkout/` | `create_order_from_cart` | Flujo completo: selección dirección, cupón, método de pago |
| `/orders/` | `OrderListView` | Listado de pedidos con filtros (Clientes: solo propios) |
| `/orders/<pk>/` | `OrderDetailView` | Detalle del pedido |
| `/orders/create/` | `OrderCreateView` | Creación manual (admin) |
| `/orders/<pk>/update/` | `OrderUpdateView` | Actualizar estado/tracking (staff) |
| `/orders/<pk>/cancel/` | `cancel_order` | Cancelación por cliente (solo pendientes, restaura stock) |

**Flujo de checkout:**
1. Validar carrito no vacío
2. Calcular subtotal, envío (gratis > $1000 MXN), impuestos (16%)
3. Aplicar cupón de descuento si existe
4. Crear pedido (status: pending, payment_status: pending)
5. Crear OrderItems desde CartItems
6. Reducir stock automáticamente
7. Vaciar carrito
8. Enviar email de confirmación
9. Redirigir a Mercado Pago si aplica

### 6.7 Mercado Pago (Pagos en Línea)

| Componente | Descripción |
|---|---|
| `create_payment_preference()` | Crea preferencia con items, payer, back_urls, webhook |
| `mp_create_preference` | Endpoint AJAX que devuelve preference_id e init_point |
| `mp_success` | Callback de pago exitoso → actualiza order a paid/confirmed |
| `mp_failure` | Callback de pago fallido → redirige al checkout |
| `mp_pending` | Callback de pago pendiente |
| `mp_webhook` | Webhook POST (CSRF exempt) para notificaciones asíncronas |
| `handle_mp_webhook()` | Procesa notificación, actualiza payment_status |

### 6.8 Cupones de Descuento

| Característica | Detalle |
|---|---|
| Tipos | Porcentaje o monto fijo |
| Validación | Fechas, usos máximos, compra mínima, activo/inactivo |
| Aplicación | En checkout, reduce el total automáticamente |
| Control | `used_count` se incrementa al aplicar |

### 6.9 Devoluciones

| Ruta | Vista | Descripción |
|---|---|---|
| `/orders/returns/` | `ReturnListView` | Listado (cliente: propios, staff: todos) |
| `/orders/returns/<pk>/` | `ReturnDetailView` | Detalle de devolución |
| `/orders/orders/<order_pk>/return/` | `ReturnCreateView` | Solicitar devolución (solo entregados/enviados) |
| `/orders/returns/<pk>/update-status/` | `update_return_status` | Staff: aprobar, recibir, reembolsar, rechazar |

**Estados de devolución:** Solicitado → Aprobado → Recibido → Reembolsado (o Rechazado)

### 6.10 Gestión de Inventario

| Ruta | Vista | Descripción |
|---|---|---|
| `/inventory/` | `inventory_dashboard` | Estadísticas: total productos, stock bajo, valor inventario, movimientos recientes, alertas activas |
| `/inventory/movements/` | `StockMovementListView` | Listado filtrable por tipo y producto |
| `/inventory/movements/create/` | `StockMovementCreateView` | Registrar entrada/salida/ajuste/devolución |
| `/inventory/alerts/` | `AlertListView` | Alertas activas |
| `/inventory/alerts/create/` | `AlertCreateView` | Crear alerta de stock mínimo |
| `/inventory/alerts/check/` | `check_inventory_alerts` | Verificar alertas manualmente |

### 6.11 Proveedores (CRUD)

| Ruta | Vista |
|---|---|
| `/inventory/suppliers/` | `SupplierListView` |
| `/inventory/suppliers/create/` | `SupplierCreateView` |
| `/inventory/suppliers/<pk>/update/` | `SupplierUpdateView` |
| `/inventory/suppliers/<pk>/delete/` | `SupplierDeleteView` |

### 6.12 Gestión de Clientes

| Ruta | Vista | Descripción |
|---|---|---|
| `/customers/` | `CustomerListView` | Listado con búsqueda (excluye staff) |
| `/customers/<pk>/` | `CustomerDetailView` | Detalle: pedidos, direcciones, wishlist |
| `/customers/profile/` | `profile_view` | Perfil combinado: datos, direcciones, wishlist |
| `/customers/register/` | `register` | Registro con creación de User + Profile + Cart + grupo Cliente |

### 6.13 Direcciones (CRUD)

| Ruta | Vista | Descripción |
|---|---|---|
| `/customers/addresses/create/` | `AddressCreateView` | Agregar dirección (envío/facturación) |
| `/customers/addresses/<pk>/update/` | `AddressUpdateView` | Editar dirección |
| `/customers/addresses/<pk>/delete/` | `AddressDeleteView` | Eliminar dirección |

### 6.14 Lista de Deseos (Wishlist)

| Ruta | Vista | Descripción |
|---|---|---|
| `/customers/wishlist/add/<product_id>/` | `wishlist_add` | Agregar producto (HTMX) |
| `/customers/wishlist/remove/<pk>/` | `wishlist_remove` | Eliminar producto |

### 6.15 Autenticación

| Ruta | Descripción |
|---|---|
| `/accounts/login/` | Inicio de sesión (Django auth) |
| `/accounts/logout/` | Cierre de sesión |
| `/accounts/password_reset/` | Recuperación de contraseña |
| `/redirect-after-login/` | Redirección post-login según rol |

---

## 7. Instalación y Configuración

### 7.1 Requisitos

- Python 3.13+
- pip
- Cuenta de Mercado Pago (para pagos)

### 7.2 Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd angelow-store

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (.env)
# Ver sección 7.3

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 7. Crear superusuario
python manage.py createsuperuser

# 8. Ejecutar servidor de desarrollo
python manage.py runserver
```

### 7.3 Variables de Entorno (.env)

```
SECRET_KEY=tu-clave-secreta-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (SQLite por defecto)
# Para PostgreSQL:
# DATABASE_URL=postgres://user:pass@host:port/dbname

# Email (Gmail SMTP recomendado)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-correo@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=ANGELOW <noreply@angelow.com>

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=TEST-xxxxxxxxxxxx
MERCADO_PAGO_PUBLIC_KEY=TEST-xxxxxxxxxxxx

# Configuración de tienda
FREE_SHIPPING_THRESHOLD=1000
SHIPPING_COST=150
TAX_RATE=0.16
```

### 7.4 Configuración de Grupos

Los grupos (Admin, Staff, Cliente) se crean automáticamente al ejecutar migraciones. Para crearlos manualmente:

```bash
python manage.py setup_groups
```

---

## 8. Pruebas

### 8.1 Configuración

- **Framework:** pytest 9.1.1 + pytest-django 4.12.0
- **Archivo de configuración:** `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = angelow.settings
python_files = tests.py
testpaths = products customers orders inventory
```

### 8.2 Tests Existentes

`products/tests.py` (177 líneas):

| Clase de Test | Pruebas |
|---|---|
| `ProductModelTest` | Creación, str, precio final, descuento, stock negativo |
| `CategoryModelTest` | str, género |
| `ProductViewTest` | Tienda pública, acceso restringido a dashboard |
| `CustomerViewTest` | Registro (GET/POST), carrito, perfil |
| `RoleBasedAccessTest` | Cliente no accede a admin, Admin sí |

### 8.3 Ejecutar Pruebas

```bash
# Todas las pruebas
pytest

# Con verbose
pytest -v

# App específica
pytest products/tests.py

# Test específico
pytest products/tests.py::ProductModelTest -v

# Con coverage
pytest --cov=.
```

### 8.4 Pruebas Pendientes

Los archivos `customers/tests.py`, `orders/tests.py` e `inventory/tests.py` existen como placeholders pero contienen pruebas mínimas o vacías. Se recomienda implementar pruebas para:

- Modelos de `orders` (Order, Cart, Coupon, Return)
- Modelos de `inventory` (StockMovement, Supplier, InventoryAlert)
- Flujo completo de checkout y pago
- Vistas de inventario y proveedores
- Vistas de clientes (direcciones, wishlist, perfil)
- Webhook de Mercado Pago
- Validaciones de formularios
- Pruebas de seguridad (acceso por roles)
