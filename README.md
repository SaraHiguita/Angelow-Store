# ANGELOW Store

Plataforma de comercio electrónico premium para la venta de ropa y accesorios de moda. Construida con **Django 6.0.3**, integración con **Mercado Pago** y experiencia de usuario moderna con **HTMX + Alpine.js**.

---

## Tabla de Contenidos

- [ANGELOW Store](#angelow-store)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Requisitos del Sistema](#requisitos-del-sistema)
  - [Instalación y Ejecución](#instalación-y-ejecución)
    - [Con Docker (recomendado)](#con-docker-recomendado)
    - [Sin Docker (desarrollo local)](#sin-docker-desarrollo-local)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Apps del Sistema](#apps-del-sistema)
    - [products](#products)
    - [customers](#customers)
    - [orders](#orders)
    - [inventory](#inventory)
  - [Modelo de Datos](#modelo-de-datos)
  - [Autenticación y Roles](#autenticación-y-roles)
  - [Reglas de Negocio](#reglas-de-negocio)
  - [Integración con Mercado Pago](#integración-con-mercado-pago)
  - [API de URLs](#api-de-urls)
  - [Plantillas y Frontend](#plantillas-y-frontend)
  - [Variables de Entorno](#variables-de-entorno)
  - [Seguridad](#seguridad)
  - [Pruebas](#pruebas)
  - [Despliegue](#despliegue)

---

## Requisitos del Sistema

- **Python** 3.12+
- **Django** 6.0.3
- **SQLite** (desarrollo) / PostgreSQL (producción)
- **Docker** y **Docker Compose** (opcional, recomendado)

---

## Instalación y Ejecución

### Con Docker (recomendado)

```bash
# Construir la imagen
docker-compose build

# Iniciar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

La aplicación estará disponible en `http://localhost:8000`.

### Sin Docker (desarrollo local)

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd angelow-store

# Crear y activar entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar servidor
python manage.py runserver
```

---

## Estructura del Proyecto

```
angelow-store/
├── angelow/                 # Configuración del proyecto
│   ├── settings.py          # Configuración general
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── products/                # Catálogo de productos
│   ├── models.py            # Category, Product, ProductImage
│   ├── views.py             # CRUD y tienda pública
│   ├── forms.py             # Formularios de productos
│   └── urls.py              # Rutas de productos
│
├── customers/               # Gestión de clientes
│   ├── models.py            # Profile, Address, Wishlist
│   ├── views.py             # Registro, perfil, wishlist
│   ├── forms.py             # Formularios de usuario/dirección
│   ├── decorators.py        # Decoradores RBAC
│   ├── signals.py           # Creación de grupos por defecto
│   └── urls.py              # Rutas de clientes
│
├── orders/                  # Órdenes y pagos
│   ├── models.py            # Order, OrderItem, Cart, CartItem, Coupon, Return
│   ├── views.py             # Carrito, checkout, órdenes, devoluciones
│   ├── mercadopago_utils.py # Integración con Mercado Pago
│   ├── forms.py             # Formularios de órdenes
│   └── urls.py              # Rutas de órdenes
│
├── inventory/               # Inventario
│   ├── models.py            # Supplier, StockMovement, InventoryAlert
│   ├── views.py             # Dashboard, movimientos, alertas
│   ├── forms.py             # Formularios de inventario
│   └── urls.py              # Rutas de inventario
│
├── templates/               # Plantillas HTML
│   ├── base.html            # Layout principal
│   ├── dashboard.html       # Dashboard admin
│   ├── shop/                # Tienda pública
│   ├── products/            # CRUD de productos
│   ├── customers/           # Perfiles y clientes
│   ├── orders/              # Carrito, checkout, órdenes
│   ├── inventory/           # Inventario y proveedores
│   ├── registration/        # Login, registro, password reset
│   ├── emails/              # Plantillas de correo
│   └── partials/            # Fragmentos HTMX
│
├── static/                  # Archivos estáticos
│   ├── css/style.css        # Estilos personalizados
│   ├── js/main.js           # JavaScript personalizado
│   └── images/              # Imágenes
│
├── media/                   # Archivos subidos por usuarios
├── staticfiles/             # Archivos estáticos recolectados
│
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Orquestación Docker
├── requirements.txt         # Dependencias Python
├── pytest.ini               # Configuración de pruebas
└── .env                     # Variables de entorno
```

---

## Apps del Sistema

### products

Catálogo de productos con categorías, imágenes múltiples y filtros.

| Modelo | Descripción |
|--------|-------------|
| `Category` | Categorías con nombre, slug, género, imagen |
| `Product` | Productos con precio, descuento, stock, tallas, colores |
| `ProductImage` | Imágenes adicionales por producto |

**Características:**
- Categorización por género (Hombre, Mujer, Unisex, Niño)
- Precio con descuento opcional
- Gestión de tallas y colores (separados por coma)
- Productos destacados en la página principal
- Filtros por categoría, género, precio y búsqueda

### customers

Gestión de usuarios, perfiles, direcciones y lista de deseos.

| Modelo | Descripción |
|--------|-------------|
| `Profile` | Datos adicionales del usuario (teléfono, avatar, preferencias) |
| `Address` | Direcciones de envío y facturación |
| `Wishlist` | Lista de deseos por usuario y producto |

**Características:**
- Registro con creación automática de perfil y carrito
- Asignación automática al grupo `Cliente`
- Direcciones múltiples con selección de dirección principal
- Lista de deseos con integración HTMX

### orders

Corazón del negocio: carrito, checkout, órdenes, cupones y devoluciones.

| Modelo | Descripción |
|--------|-------------|
| `Cart` | Carrito de compras (OneToOne con User) |
| `CartItem` | Items en el carrito (producto + talla + color) |
| `Order` | Órdenes de compra con ciclo de vida completo |
| `OrderItem` | Items de la orden |
| `Coupon` | Cupones de descuento (porcentaje o fijo) |
| `Return` | Devoluciones y reembolsos |

**Características:**
- Carrito con Alpine.js para conteo en vivo
- Checkout con cálculo de subtotal, IVA (16%), envío y descuento
- Integración con Mercado Pago (pago en línea) y pago contra entrega
- Cupones de descuento con validación de vigencia y uso máximo
- Devoluciones con flujo de aprobación por staff
- Envío de correo de confirmación

### inventory

Control de inventario, proveedores y alertas de stock bajo.

| Modelo | Descripción |
|--------|-------------|
| `Supplier` | Proveedores con datos de contacto |
| `StockMovement` | Movimientos de stock (entrada, salida, ajuste, devolución) |
| `InventoryAlert` | Alertas de stock mínimo por producto |

**Características:**
- Actualización automática de stock en cada movimiento
- Validación de stock suficiente para movimientos de salida
- Alertas configurables por producto (umbral por defecto: 10)
- Dashboard con estadísticas de inventario

---

## Modelo de Datos

### Diagrama de Relaciones

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Category  │       │   Product   │       │ ProductImage│
│─────────────│       │─────────────│       │─────────────│
│ name        │──1:N──│ name        │──1:N──│ image       │
│ slug        │       │ slug        │       │ alt_text    │
│ gender      │       │ sku         │       │ order       │
│ description │       │ price       │       └─────────────┘
│ image       │       │ discount_   │
└─────────────┘       │ price       │
                      │ stock_qty   │       ┌─────────────┐
                      │ sizes       │───────│  Wishlist   │
                      │ colors      │   N:N │─────────────│
                      │ category ───│       │ user        │
                      │ status      │       │ product     │
                      └──────┬──────┘       │ notes       │
                             │              └─────────────┘
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────┴──────┐ ┌─────┴─────┐ ┌──────┴──────┐
       │  CartItem   │ │ OrderItem │ │StockMovement│
       │─────────────│ │───────────│ │─────────────│
       │ cart        │ │ order     │ │ product     │
       │ product     │ │ product   │ │ movement_typ│
       │ quantity    │ │ quantity  │ │ quantity    │
       │ size        │ │ size      │ │ unit_cost   │
       │ color       │ │ color     │ │ supplier ───│──┐
       └──────┬──────┘ │ unit_price│ └─────────────┘  │
              │         │ total_pr. │                  │
       ┌──────┴──────┐ └─────┬─────┘           ┌──────┴──────┐
       │    Cart     │       │                  │  Supplier   │
       │─────────────│       │                  │─────────────│
       │ user (1:1)  │       │                  │ name        │
       └─────────────┘       │                  │ contact     │
                             │                  │ email       │
       ┌─────────────┐       │                  │ phone       │
       │    Order    │◄──────┘                  │ tax_id      │
       │─────────────│                          └─────────────┘
       │ order_number│       ┌─────────────┐
       │ user        │──1:N──│  Return     │
       │ status      │       │─────────────│
       │ payment_    │       │ order       │
       │  status     │       │ reason      │
       │ subtotal    │       │ status      │
       │ shipping_   │       │ refund_amt  │
       │  cost       │       └─────────────┘
       │ tax         │
       │ discount    │       ┌─────────────┐
       │ total       │       │   Coupon    │
       └─────────────┘       │─────────────│
                             │ code        │
       ┌─────────────┐       │ type        │
       │   Profile   │       │ value       │
       │─────────────│       │ max_uses    │
       │ user (1:1)──│──┐    │ valid_from  │
       │ phone       │  │    │ valid_to    │
       │ birth_date  │  │    └─────────────┘
       │ avatar      │  │
       │ preferences │  │    ┌─────────────┐
       │ newsletter  │  │    │  Address    │
       └─────────────┘  │    │─────────────│
                        ├────│ user        │
       ┌─────────────┐  │    │ type        │
       │  auth.User  │◄─┘    │ street      │
       │─────────────│       │ city        │
       │ username    │       │ state       │
       │ email       │       │ zip_code    │
       │ groups      │       │ is_default  │
       └─────────────┘       └─────────────┘
```

---

## Autenticación y Roles

El sistema implementa un control de acceso basado en roles (RBAC) con tres grupos creados automáticamente mediante una señal `post_migrate`:

| Grupo | Acceso |
|-------|--------|
| **Admin** | Acceso total (superuser). Sin permisos explícitos en el grupo. |
| **Staff** | 29 permisos: CRUD en productos, categorías, órdenes, carritos, proveedores, movimientos, alertas, perfiles, direcciones, usuarios, cupones y devoluciones. |
| **Cliente** | Sin permisos administrativos. Acceso a tienda, perfil, pedidos propios. |

### Flujo de autenticación

1. **Registro**: Crea `User` + `Profile` + `Cart`, asigna grupo `Cliente`, inicia sesión automáticamente.
2. **Login**: Usa `django.contrib.auth.views.LoginView` en `/accounts/login/`.
3. **Post-login**: `role_redirect` redirige según el rol:
   - Admin → Dashboard (`/`)
   - Staff → Inventario (`/inventory/`)
   - Cliente → Tienda (`/tienda/`)
4. **Logout**: POST a `/accounts/logout/`.

### Decoradores y Mixins

- `@admin_required` / `AdminRequiredMixin` — solo superuser o grupo Admin
- `@staff_required` / `StaffRequiredMixin` — superuser, Admin o Staff
- `@login_required` — cualquier usuario autenticado

---

## Reglas de Negocio

| # | Regla |
|---|-------|
| 1 | **Envío gratis** en órdenes ≥ $1,000 MXN |
| 2 | **IVA del 16%** sobre el subtotal |
| 3 | **Número de orden**: formato `ANG{10000 + id}` |
| 4 | **Stock**: se reduce al crear la orden, se restaura al cancelar |
| 5 | **Devoluciones**: solo en órdenes entregadas/enviadas |
| 6 | **Cancelaciones**: solo en órdenes pendientes |
| 7 | **Cupones**: validan vigencia, usos máximos y compra mínima |
| 8 | **Descuento**: `discount_price` anula `price` si es menor |
| 9 | **Dirección principal**: al marcar una, se desmarcan las demás del mismo tipo |
| 10 | **Carrito**: mismo producto + talla + color incrementa cantidad |
| 11 | **Perfil y Carrito** se crean automáticamente al registrarse |
| 12 | **Cliente** solo ve sus propias órdenes; **Staff/Admin** ven todas |

---

## Integración con Mercado Pago

El proyecto integra **Mercado Pago** como pasarela de pago mediante el SDK oficial (`mercadopago==3.2.0`).

### Flujo de pago

1. El usuario selecciona "Mercado Pago" en el checkout
2. La vista `mp_create_preference` crea una preferencia de pago
3. Se redirige al usuario a la URL de `init_point` de Mercado Pago
4. El usuario paga en la plataforma de Mercado Pago
5. Al aprobarse, se redirige a `mp_success` que actualiza la orden
6. **Webhook**: `mp_webhook` recibe notificaciones IPN y actualiza `payment_status`

### Configuración

Variables en `.env`:
```
MERCADO_PAGO_ACCESS_TOKEN=TEST-...
MERCADO_PAGO_PUBLIC_KEY=TEST-...
```

### Endpoints

| Ruta | Propósito |
|------|-----------|
| `/orders/mp-create-preference/<order_id>/` | Crea preferencia (JSON) |
| `/orders/mp-success/<order_id>/` | Redirección post-pago exitoso |
| `/orders/mp-failure/<order_id>/` | Redirección post-pago fallido |
| `/orders/mp-pending/<order_id>/` | Redirección post-pago pendiente |
| `/orders/mp-webhook/` | Webhook IPN (POST, `@csrf_exempt`) |

---

## API de URLs

### Rutas principales

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/admin/` | Admin de Django | Panel administrativo |
| `/` | `dashboard` | Dashboard admin/staff |
| `/tienda/` | `shop_home` | Tienda pública |
| `/tienda/productos/` | `shop_product_list` | Lista pública de productos |
| `/tienda/productos/<slug:slug>/` | `shop_product_detail` | Detalle de producto |
| `/accounts/login/` | LoginView | Inicio de sesión |
| `/accounts/logout/` | LogoutView | Cierre de sesión |
| `/accounts/password_reset/` | PasswordResetView | Recuperar contraseña |
| `/redirect-after-login/` | `role_redirect` | Redirección post-login |

### Módulo customers

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/customers/register/` | `register` | Registro de usuario |
| `/customers/profile/` | `profile_view` | Perfil de usuario |
| `/customers/` | `CustomerListView` | Lista de clientes (staff) |
| `/customers/<pk>/` | `CustomerDetailView` | Detalle de cliente (staff) |
| `/customers/addresses/create/` | `AddressCreateView` | Nueva dirección |
| `/customers/addresses/<pk>/update/` | `AddressUpdateView` | Editar dirección |
| `/customers/addresses/<pk>/delete/` | `AddressDeleteView` | Eliminar dirección |
| `/customers/wishlist/add/<product_id>/` | `wishlist_add` | Agregar a wishlist |
| `/customers/wishlist/remove/<pk>/` | `wishlist_remove` | Quitar de wishlist |

### Módulo orders

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/orders/cart/` | `cart_view` | Ver carrito |
| `/orders/cart/add/<product_id>/` | `add_to_cart` | Agregar al carrito |
| `/orders/cart/update/<pk>/` | `update_cart_item` | Actualizar cantidad |
| `/orders/cart/remove/<pk>/` | `remove_from_cart` | Eliminar del carrito |
| `/orders/checkout/` | `create_order_from_cart` | Finalizar compra |
| `/orders/` | `OrderListView` | Lista de órdenes |
| `/orders/<pk>/` | `OrderDetailView` | Detalle de orden |
| `/orders/<pk>/cancel/` | `cancel_order` | Cancelar orden |
| `/orders/returns/` | `ReturnListView` | Lista de devoluciones |
| `/orders/returns/<pk>/` | `ReturnDetailView` | Detalle de devolución |

### Módulo products

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/categories/` | `CategoryListView` | Lista de categorías |
| `/categories/create/` | `CategoryCreateView` | Nueva categoría |
| `/categories/<slug:slug>/` | `CategoryDetailView` | (no listado) |
| `/products/` | `ProductListView` | Lista de productos |
| `/products/create/` | `ProductCreateView` | Nuevo producto |
| `/products/<slug:slug>/` | `ProductDetailView` | Detalle de producto |
| `/products/<slug:slug>/update/` | `ProductUpdateView` | Editar producto |
| `/products/<slug:slug>/delete/` | `ProductDeleteView` | Eliminar producto |

### Módulo inventory

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/inventory/` | `inventory_dashboard` | Dashboard de inventario |
| `/inventory/suppliers/` | `SupplierListView` | Proveedores |
| `/inventory/movements/` | `StockMovementListView` | Movimientos de stock |
| `/inventory/movements/create/` | `StockMovementCreateView` | Nuevo movimiento |
| `/inventory/alerts/` | `AlertListView` | Alertas de stock |
| `/inventory/alerts/create/` | `AlertCreateView` | Nueva alerta |
| `/inventory/alerts/check/` | `check_inventory_alerts` | Verificar alertas |

---

## Plantillas y Frontend

### Tecnologías frontend

- **Bootstrap 5.3** — framework CSS
- **HTMX 2.0.4** — interacciones dinámicas sin JavaScript
- **Alpine.js 3.14.8** — reactividad en el cliente
- **Playfair Display + Inter** — tipografía
- **Bootstrap Icons** — iconografía

### Estructura de plantillas (46 archivos)

```
templates/
├── base.html                  # Layout principal con navbar y footer
├── dashboard.html             # Dashboard admin/staff
├── shop/                      # Tienda pública (3)
│   ├── home.html              # Página principal
│   ├── product_list.html      # Lista de productos con filtros
│   └── product_detail.html    # Detalle de producto
├── products/                  # CRUD productos (6)
├── customers/                 # Perfiles y clientes (5)
├── orders/                    # Carrito, checkout, órdenes (11)
├── inventory/                 # Inventario y proveedores (7)
├── registration/              # Login, registro, password reset (6)
├── emails/                    # Plantillas de correo (1)
└── partials/                  # Fragmentos HTMX (1)
```

### Características del frontend

- **Navbar con vidrio esmerilado** (glassmorphism)
- **Carrito en vivo**: Alpine.js actualiza el contador al agregar/eliminar productos
- **Filtros con debounce**: búsqueda y filtros de precio con Alpine.js `@input.debounce`
- **Galería de imágenes**: selector de imágenes con Alpine.js
- **Selectores de talla y color**: botones interactivos
- **HTMX boost**: navegación tipo SPA con `hx-boost`
- **Mensajes dinámicos**: alertas con cierre automático y soporte HTMX OOB swap
- **Diseño responsive**: adaptado a dispositivos móviles

### Estilos personalizados (`static/css/style.css`)

- 492 líneas de CSS con variables y diseño premium
- Paleta de colores: fondo oscuro `#1a1a2e`, acentos dorados `#c9a962`
- Tipografía serif para marca, sans-serif para contenido
- Animaciones y transiciones suaves
- Tarjetas de producto con efecto hover

---

## Variables de Entorno

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `SECRET_KEY` | `django-insecure-...` | Clave secreta de Django |
| `DEBUG` | `True` | Modo depuración |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos |
| `MERCADO_PAGO_ACCESS_TOKEN` | `TEST-...` | Token de acceso MP |
| `MERCADO_PAGO_PUBLIC_KEY` | `TEST-...` | Llave pública MP |
| `EMAIL_BACKEND` | `console.EmailBackend` | Backend de correo |
| `EMAIL_HOST` | `smtp.gmail.com` | Servidor SMTP |
| `EMAIL_PORT` | `587` | Puerto SMTP |
| `EMAIL_USE_TLS` | `True` | TLS para correo |
| `EMAIL_HOST_USER` | `` | Usuario SMTP |
| `EMAIL_HOST_PASSWORD` | `` | Contraseña SMTP |
| `DEFAULT_FROM_EMAIL` | `ANGELOW <noreply@...>` | Remitente por defecto |
| `FREE_SHIPPING_THRESHOLD` | `1000` | Umbral de envío gratis |
| `SHIPPING_COST` | `150` | Costo de envío |
| `TAX_RATE` | `0.16` | Tasa de IVA (16%) |

---

## Seguridad

| Medida | Implementación |
|--------|----------------|
| **CSRF** | Cookies HttpOnly, SameSite=Lax |
| **Sesión** | 24h de duración, expira al cerrar navegador, HttpOnly, SameSite=Lax |
| **SSL** | Redirección en producción, HSTS 1 año, preload |
| **Rate limiting** | Endpoint de login (solo producción) |
| **CSP** | Content Security Policy con `django-csp` |
| **RBAC** | 3 grupos con decoradores y mixins |
| **Stock** | Validación antes de movimientos de salida |
| **Webhook** | `@csrf_exempt` en webhook de pagos (estándar IPN) |
| **Producción** | `SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`, HSTS |
| **Contraseñas** | Validadores: similitud, longitud mínima, comunes, numéricas |

---

## Pruebas

El proyecto usa **pytest** con `pytest-django`.

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas de una app específica
pytest products/
pytest customers/
pytest orders/
pytest inventory/

# Con cobertura (si está instalado)
pytest --cov=.
```

Configuración en `pytest.ini`:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = angelow.settings
testpaths = products customers orders inventory
python_files = tests.py
```

---

## Despliegue

### Docker (producción)

```bash
# Construir con variables de producción
DEBUG=False docker-compose up -d --build

# O directamente
docker build -t angelow-store .
docker run -d -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=... \
  -e ALLOWED_HOSTS=... \
  -e MERCADO_PAGO_ACCESS_TOKEN=... \
  -v db_data:/app/db.sqlite3 \
  angelow-store
```

### Servidor tradicional

1. Configurar PostgreSQL y actualizar `DATABASES` en `settings.py`
2. Configurar servidor web (Nginx + Gunicorn/uWSGI)
3. Configurar HTTPS con Let's Encrypt
4. Ajustar `DEBUG=False`, `ALLOWED_HOSTS`, `SECRET_KEY`
5. Ejecutar migraciones y recolectar estáticos
6. Configurar tareas cron para alertas de inventario si es necesario

---

## Dependencias

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Django | 6.0.3 | Framework web |
| pillow | 12.1.1 | Procesamiento de imágenes |
| crispy-bootstrap5 | 2026.3 | Formularios Bootstrap 5 |
| django-crispy-forms | 2.6 | Renderizado de formularios |
| python-decouple | 3.8 | Variables de entorno |
| django-htmx | 1.27.0 | Integración HTMX |
| django-csp | 4.0 | Content Security Policy |
| django-ratelimit | 4.1.0 | Límite de peticiones |
| mercadopago | 3.2.0 | SDK Mercado Pago |
| whitenoise | 6.12.0 | Archivos estáticos |
| httpx | 0.28.1 | Cliente HTTP |
| pytest | 9.1.1 | Testing |
| pytest-django | 4.12.0 | Integración Django + pytest |

---

## Licencia

Todos los derechos reservados © 2026 ANGELOW.
