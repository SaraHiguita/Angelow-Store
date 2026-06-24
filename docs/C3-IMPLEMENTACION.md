# C3 — Implementación del Proyecto

## ANGELOW Store — Plataforma de Comercio Electrónico Premium

---

## 1. Metodología de Desarrollo

### 1.1 Metodología Utilizada

El proyecto se desarrolló siguiendo una metodología **ágil adaptada** con iteraciones cortas (sprints de 1 semana) y entregables incrementales. Se aplicaron principios de **Desarrollo Guiado por Pruebas (TDD)** donde fue posible, y **Desarrollo Iterativo** para los módulos funcionales.

### 1.2 Ciclo de Desarrollo

1. **Análisis** — Identificación de requisitos y casos de uso
2. **Diseño** — Modelado de datos, arquitectura, maquetado de interfaces
3. **Implementación** — Codificación con Django (modelos → vistas → URLs → templates)
4. **Pruebas** — Tests unitarios y de integración
5. **Revisión** — Validación funcional y de seguridad
6. **Despliegue** — Contenedorización con Docker

---

## 2. Detalle de Implementación por Módulo

### 2.1 Módulo de Productos (`products`)

#### Archivos implementados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `models.py` | 111 | Category, Product, ProductImage |
| `views.py` | 216 | CRUD staff + vistas tienda pública |
| `forms.py` | 120 | Formularios con validaciones |
| `urls.py` | 50 | Enrutamiento del módulo |
| `admin.py` | — | Registro en Django Admin |
| `tests.py` | 177 | Tests unitarios y de integración |

#### Modelos

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    main_image = models.ImageField(upload_to='products/main/', blank=True)
    sizes = models.CharField(max_length=200, blank=True, help_text='Separadas por coma')
    colors = models.CharField(max_length=200, blank=True, help_text='Separados por coma')
    material = models.CharField(max_length=100, blank=True)
    stock_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_final_price(self):
        return self.discount_price if self.discount_price and self.is_on_sale() else self.price

    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price
```

#### Vistas destacadas

- **`dashboard()`** — Vista principal con estadísticas: total productos, alertas de stock bajo (stock < umbral), pedidos pendientes, total clientes, productos recientes, pedidos recientes. Requiere `@staff_required`.
- **`shop_home()`** — Página principal pública con productos activos, categorías filtradas por género, productos destacados y latest products.
- **`shop_product_list()`** — Listado público con filtros combinados: categoría, género, búsqueda por nombre, rango de precio mínimo y máximo. Paginación de 12 productos por página.
- **`shop_product_detail()`** — Detalle de producto con galería de imágenes, productos relacionados de la misma categoría y excluyendo el actual.

### 2.2 Módulo de Clientes (`customers`)

#### Archivos implementados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `models.py` | 65 | Profile, Address, Wishlist |
| `views.py` | 210 | Registro, perfil, direcciones, wishlist |
| `forms.py` | 63 | Formularios con validaciones |
| `urls.py` | 23 | Enrutamiento |
| `decorators.py` | 54 | Decoradores y mixins de roles |
| `signals.py` | 33 | Creación automática de grupos y permisos |
| `context_processors.py` | 8 | Contador de carrito global |

#### Decoradores de Roles

```python
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())

def is_staff(user):
    return user.is_authenticated and (
        user.is_superuser or
        user.groups.filter(name='Staff').exists() or
        user.groups.filter(name='Admin').exists()
    )

def staff_required(view_func=None, login_url=None, raise_exception=False):
    actual_decorator = user_passes_test(is_staff, login_url=login_url, redirect_field_name=None)
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
```

#### Señal de Post-Migrate

```python
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != 'customers':
        return
    # Crea Admin, Staff (con permisos granulares), Cliente
    Group.objects.get_or_create(name='Admin')
    staff_group, _ = Group.objects.get_or_create(name='Staff')
    # Asigna 28 permisos específicos al grupo Staff
    staff_codenames = ['view_category', 'add_category', ..., 'delete_return']
    perms = Permission.objects.filter(codename__in=staff_codenames)
    staff_group.permissions.add(*perms)
    Group.objects.get_or_create(name='Cliente')
```

#### Flujo de Registro

```python
def register(request):
    if request.method == 'POST':
        # Validar campos (username, email, password1, password2)
        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.get_or_create(user=user)
        Cart.objects.get_or_create(user=user)
        cliente_group = Group.objects.get(name='Cliente')
        user.groups.add(cliente_group)
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        return redirect('shop_home')
```

### 2.3 Módulo de Pedidos (`orders`)

#### Archivos implementados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `models.py` | 230 | Cart, CartItem, Order, OrderItem, Coupon, Return |
| `views.py` | 480 | Carrito, checkout, pedidos, devoluciones, MP |
| `mercadopago_utils.py` | 73 | SDK Mercado Pago |
| `urls.py` | ~40 | Enrutamiento |
| `forms.py` | — | Formularios |

#### Modelo Order con generación automática de order_number

```python
class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # ... más campos

    def save(self, *args, **kwargs):
        if not self.order_number:
            last = Order.objects.all().order_by('id').last()
            last_id = last.id + 1 if last else 1
            self.order_number = f'ANG{10000 + last_id}'
        self.total = self.subtotal + self.shipping_cost + self.tax - self.discount
        super().save(*args, **kwargs)
```

#### Checkout (Flujo completo)

```python
def create_order_from_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart')

    if request.method == 'POST':
        # 1. Calcular subtotal desde items del carrito
        subtotal = sum(item.product.get_final_price() * item.quantity for item in cart_items)

        # 2. Aplicar cupón si existe
        discount = _apply_coupon(coupon_code, subtotal) if coupon_code else Decimal('0')

        # 3. Calcular envío e impuestos
        shipping_cost = Decimal('0') if subtotal >= FREE_SHIPPING_THRESHOLD else Decimal(str(SHIPPING_COST))
        tax = (subtotal - discount) * Decimal(str(TAX_RATE))

        # 4. Crear Order
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal, shipping_cost=shipping_cost,
            tax=tax, discount=discount, total=subtotal + shipping_cost + tax - discount,
            shipping_address=shipping_addr, billing_address=billing_addr,
            payment_method=payment_method, status='pending', payment_status='pending'
        )

        # 5. Crear OrderItems y reducir stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity,
                size=item.size, color=item.color, unit_price=item.product.get_final_price()
            )
            _reduce_stock(item.product, item.quantity, request.user)

        # 6. Vaciar carrito y redirigir
        cart_items.delete()
        # Enviar email, redirigir a MP si aplica
```

#### Integración Mercado Pago

```python
# mercadopago_utils.py
def create_payment_preference(order, request):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    preference_data = {
        "items": [
            {
                "title": item.product.name,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "currency_id": "MXN",
            }
            for item in order.items.all()
        ],
        "payer": {"email": order.user.email, "name": order.user.first_name},
        "back_urls": {
            "success": request.build_absolute_uri(reverse('mp_success', args=[order.id])),
            "failure": request.build_absolute_uri(reverse('mp_failure', args=[order.id])),
            "pending": request.build_absolute_uri(reverse('mp_pending', args=[order.id])),
        },
        "notification_url": request.build_absolute_uri(reverse('mp_webhook')),
        "auto_return": "approved",
    }
    result = sdk.preference().create(preference_data)
    return result["response"]
```

### 2.4 Módulo de Inventario (`inventory`)

#### Archivos implementados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `models.py` | 95 | Supplier, StockMovement, InventoryAlert |
| `views.py` | 154 | Dashboard, CRUD de suppliers, movimientos, alertas |
| `urls.py` | ~25 | Enrutamiento |
| `forms.py` | — | Formularios |

#### StockMovement con actualización automática de stock

```python
class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # Validar stock suficiente para salidas
        if self.movement_type == 'out' and self.product.stock_quantity < abs(self.quantity):
            raise ValidationError('Stock insuficiente.')

        # Calcular total_cost
        if self.unit_cost:
            self.total_cost = abs(self.quantity) * self.unit_cost

        super().save(*args, **kwargs)

        # Actualizar stock del producto
        product = self.product
        if self.movement_type == 'in':
            product.stock_quantity += self.quantity
        elif self.movement_type == 'out':
            product.stock_quantity -= abs(self.quantity)
        elif self.movement_type == 'return':
            product.stock_quantity += abs(self.quantity)
        elif self.movement_type == 'adjustment':
            product.stock_quantity = abs(self.quantity)
        product.save()
```

---

## 3. Frontend e Interactividad

### 3.1 HTMX — Interacciones Asíncronas

| Funcionalidad | Disparador | Destino | Comportamiento |
|---------------|-----------|---------|----------------|
| Agregar al carrito | `hx-post="/orders/cart/add/<id>/"` | `#messages-container` | Agrega producto, muestra mensaje |
| Actualizar cantidad | `hx-post="/orders/cart/update/<pk>/"` | `#cart-items` | Actualiza cantidad o elimina |
| Eliminar del carrito | `hx-get="/orders/cart/remove/<pk>/"` | `#cart-items` | Elimina item |
| Agregar a wishlist | `hx-post="/customers/wishlist/add/<id>/"` | `#messages-container` | Agrega a deseos |

### 3.2 Alpine.js — Estado Reactivo

| Componente | Estado | Comportamiento |
|------------|--------|----------------|
| Contador carrito | `x-data="{ cartCount: {{ cart_count }} }"` | Se actualiza con HTMX OOB |
| Selector de talla | `x-model="selectedSize"` | Cambia clase activa visual |
| Selector de color | `x-model="selectedColor"` | Cambia clase activa visual |
| Selector de cantidad | `x-model.number="quantity"` | Incrementa/decrementa |

### 3.3 Template Base (`base.html`)

La plantilla base incluye:
- **Bootstrap 5.3** CDN para layout responsive
- **HTMX 2.0** para interacciones AJAX sin JavaScript
- **Alpine.js 3.14** para estado reactivo del cliente
- **Google Fonts** (Playfair Display + Inter)
- **Navbar** con navegación contextual según rol del usuario
- **Footer** con copyright
- **Contenedor de mensajes** para flash messages y HTMX OOB swaps
- **Badge de carrito** con Alpine.js para contador en vivo

---

## 4. Seguridad Implementada

### 4.1 Control de Acceso (RBAC)

```
Usuario → Autenticación → Login
    │
    ├── Superuser → Admin (acceso total)
    │
    ├── Grupo 'Admin' → Dashboard + CRUD + Django Admin
    │
    ├── Grupo 'Staff' → Dashboard + CRUD (productos, pedidos, inventario, clientes)
    │
    └── Grupo 'Cliente' → Tienda pública, perfil propio, pedidos propios
```

### 4.2 Protecciones por Capa

| Capa | Medida |
|------|--------|
| Modelo | Validación de stock no negativo, precios positivos |
| Formulario | Validación de email único, teléfono, código postal |
| Vista | `@login_required`, `@staff_required`, filtrado por usuario |
| URL | Patrones protegidos, rutas separadas por rol |
| Middleware | CSRF, sesión, seguridad, CSP |
| Cookie | HttpOnly, SameSite, Secure (producción) |

### 4.3 Rate Limiting

```python
# settings.py (producción)
if not DEBUG:
    RATELIMIT_ENABLE = True
    RATELIMIT_USE_CACHE = 'default'
    RATELIMIT_VIEW = 'login'
```

---

## 5. Dockerización

### 5.1 Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/media /app/staticfiles /app/cache && \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
```

### 5.2 Docker Compose

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./db.sqlite3:/app/db.sqlite3
      - media_data:/app/media
      - static_data:/app/staticfiles
      - cache_data:/app/cache
    env_file:
      - .env
    environment:
      - DEBUG=True
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
    command: >
      sh -c "
        python manage.py migrate --noinput &&
        python manage.py runserver 0.0.0.0:8000
      "

volumes:
  media_data:
  static_data:
  cache_data:
```

### 5.3 .dockerignore

```
venv/
__pycache__/
*.pyc
*.pyo
.env
.git/
.gitignore
.pytest_cache/
.DS_Store
*.docx
DOCUMENTATION.md
```

---

## 6. Pruebas

### 6.1 Configuración (`pytest.ini`)

```ini
[pytest]
DJANGO_SETTINGS_MODULE = angelow.settings
python_files = tests.py
testpaths = products customers orders inventory
```

### 6.2 Tests Implementados (`products/tests.py`)

| Clase | Pruebas | Resultado esperado |
|-------|---------|-------------------|
| `ProductModelTest` | Creación de producto, string representation, precio final con/sin descuento, stock negativo | Validaciones correctas |
| `CategoryModelTest` | Creación, string, género | Modelo funcional |
| `ProductViewTest` | Tienda pública carga, dashboard requiere login | Vistas funcionan |
| `CustomerViewTest` | Registro GET/POST, carrito tras registro, vista perfil | Flujo registro OK |
| `RoleBasedAccessTest` | Cliente no accede a admin, Admin sí | RBAC funcional |

### 6.3 Resultados

```
pytest -v
============================= test session starts ==============================
collected 17 items

products/tests.py::ProductModelTest::test_product_creation PASSED
products/tests.py::ProductModelTest::test_product_str PASSED
products/tests.py::ProductModelTest::test_final_price_without_discount PASSED
products/tests.py::ProductModelTest::test_final_price_with_discount PASSED
products/tests.py::ProductModelTest::test_negative_stock PASSED
products/tests.py::CategoryModelTest::test_category_creation PASSED
products/tests.py::CategoryModelTest::test_category_str PASSED
products/tests.py::CategoryModelTest::test_gender_choices PASSED
products/tests.py::ProductViewTest::test_shop_home_status PASSED
products/tests.py::ProductViewTest::test_dashboard_requires_login PASSED
products/tests.py::ProductViewTest::test_dashboard_staff_access PASSED
products/tests.py::CustomerViewTest::test_register_view_get PASSED
products/tests.py::CustomerViewTest::test_register_view_post PASSED
products/tests.py::CustomerViewTest::test_cart_created_after_register PASSED
products/tests.py::CustomerViewTest::test_profile_requires_login PASSED
products/tests.py::RoleBasedAccessTest::test_cliente_no_access_to_dashboard PASSED
products/tests.py::RoleBasedAccessTest::test_admin_access_to_dashboard PASSED

============================== 17 passed in 7.32s ==============================
```

---

## 7. Variables de Entorno

```
SECRET_KEY=clave-secreta-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MERCADO_PAGO_ACCESS_TOKEN=TEST-xxx
MERCADO_PAGO_PUBLIC_KEY=TEST-xxx

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=ANGELOW <noreply@angelow.com>

FREE_SHIPPING_THRESHOLD=1000
SHIPPING_COST=150
TAX_RATE=0.16
```

---

## 8. Resultados y Conclusiones

### 8.1 Resultados Obtenidos

| Objetivo | Estado | Entregable |
|----------|--------|------------|
| Catálogo de productos con categorías | ✅ | CRUD completo, tienda pública con filtros |
| Sistema de inventario con alertas | ✅ | Movimientos, proveedores, alertas de stock |
| Módulo de clientes | ✅ | Registro, perfiles, direcciones, wishlist |
| Flujo de compras con pagos | ✅ | Carrito, checkout, MP, pedidos |
| Pedidos y devoluciones | ✅ | Trazabilidad, emails, cancelaciones |
| Control de acceso (RBAC) | ✅ | 3 roles con decoradores y mixins |
| Dockerización | ✅ | Contenedor reproducible |
| Pruebas | ✅ | 17 tests pasando |

### 8.2 Lecciones Aprendidas

1. **Arquitectura modular**: Separar la lógica en 4 apps Django facilitó el desarrollo paralelo y el mantenimiento.
2. **HTMX + Alpine.js**: Combinación liviana y efectiva para interactividad sin SPA, ideal para proyectos Django.
3. **Señales post_migrate**: Útiles para crear datos iniciales (grupos, permisos), pero deben estar bien aisladas por app.
4. **Stock movements como source of truth**: Mantener un registro de auditoría de todos los cambios de stock es crucial para la integridad del inventario.
5. **Validaciones en múltiples capas**: Combinar validaciones en modelo, formulario y vista proporciona defensa en profundidad.

### 8.3 Recomendaciones Futuras

1. Migrar a PostgreSQL para producción (escalabilidad, integridad referencial)
2. Implementar pruebas para `orders` e `inventory` (actualmente placeholders)
3. Agregar login social (Google, Facebook) para facilitar el registro
4. Implementar facturación electrónica (CFDI/DIAN)
5. Agregar panel de analytics con gráficos (Chart.js)
6. Implementar caché con Redis para mejorar rendimiento
7. Agregar webhooks de proveedores para automatizar reposiciones
8. Implementar cola de tareas (Celery) para envío de emails asíncrono

---

## 9. Glosario

| Término | Definición |
|---------|------------|
| MVT | Model-View-Template, patrón arquitectónico de Django |
| ORM | Object-Relational Mapping, capa de abstracción de base de datos |
| RBAC | Role-Based Access Control, control de acceso basado en roles |
| CRUD | Create, Read, Update, Delete — operaciones básicas de persistencia |
| CSP | Content Security Policy, política de seguridad de contenido |
| CSRF | Cross-Site Request Forgery, falsificación de petición entre sitios |
| HTMX | Librería que permite interacciones AJAX directamente en HTML |
| MP | Mercado Pago, pasarela de pagos latinoamericana |
| SKU | Stock Keeping Unit, código único de producto |
| IPN | Instant Payment Notification, notificación instantánea de pago |
| WBS | Work Breakdown Structure, estructura de desglose del trabajo |
