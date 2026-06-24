# C2 — Planificación del Proyecto

## ANGELOW Store — Plataforma de Comercio Electrónico Premium

---

## 1. Estructura de Desglose del Trabajo (EDT / WBS)

```
ANGELOW Store
│
├── 1.0 Gestión del Proyecto
│   ├── 1.1 Planificación
│   ├── 1.2 Seguimiento
│   └── 1.3 Documentación
│
├── 2.0 Configuración del Entorno
│   ├── 2.1 Instalación de herramientas (Python, Django, Docker)
│   ├── 2.2 Creación del proyecto Django
│   └── 2.3 Configuración de base de datos y .env
│
├── 3.0 Módulo de Productos (products)
│   ├── 3.1 Modelos (Category, Product, ProductImage)
│   ├── 3.2 Vistas CRUD (staff)
│   ├── 3.3 Vistas de tienda pública
│   ├── 3.4 Formularios con validaciones
│   ├── 3.5 Plantillas HTML
│   └── 3.6 URLs y routing
│
├── 4.0 Módulo de Clientes (customers)
│   ├── 4.1 Modelos (Profile, Address, Wishlist)
│   ├── 4.2 Sistema de registro y autenticación
│   ├── 4.3 Gestión de perfil y direcciones
│   ├── 4.4 Lista de deseos
│   ├── 4.5 Señales para grupos y permisos
│   ├── 4.6 Decoradores de roles (Admin/Staff/Cliente)
│   ├── 4.7 Context processor del carrito
│   └── 4.8 Plantillas HTML
│
├── 5.0 Módulo de Pedidos (orders)
│   ├── 5.1 Modelos (Cart, CartItem, Order, OrderItem, Coupon, Return)
│   ├── 5.2 Carrito de compras (add/update/remove con HTMX)
│   ├── 5.3 Checkout (dirección, cupón, cálculo de totales)
│   ├── 5.4 Integración Mercado Pago
│   ├── 5.5 Gestión de pedidos (staff)
│   ├── 5.6 Devoluciones
│   ├── 5.7 Cancelación y restauración de stock
│   └── 5.8 Plantillas HTML
│
├── 6.0 Módulo de Inventario (inventory)
│   ├── 6.1 Modelos (Supplier, StockMovement, InventoryAlert)
│   ├── 6.2 CRUD de proveedores
│   ├── 6.3 Movimientos de stock (entrada/salida/ajuste)
│   ├── 6.4 Alertas de stock mínimo
│   ├── 6.5 Dashboard de inventario
│   └── 6.6 Plantillas HTML
│
├── 7.0 Dashboard y Estadísticas
│   ├── 7.1 Dashboard principal (productos, pedidos, clientes, alertas)
│   └── 7.2 Dashboard de inventario
│
├── 8.0 Seguridad
│   ├── 8.1 CSRF, sesiones, cookies seguras
│   ├── 8.2 Rate limiting (login)
│   ├── 8.3 Content Security Policy (CSP)
│   ├── 8.4 SSL/HSTS (producción)
│   └── 8.5 Validación por roles en vistas
│
├── 9.0 Frontend y Experiencia de Usuario
│   ├── 9.1 Plantilla base (base.html con navbar, footer)
│   ├── 9.2 Tema visual premium (CSS personalizado)
│   ├── 9.3 Interacciones HTMX (carrito, wishlist)
│   ├── 9.4 Estado reactivo con Alpine.js
│   └── 9.5 Diseño responsive (Bootstrap 5)
│
├── 10.0 Infraestructura y Despliegue
│   ├── 10.1 Dockerfile
│   ├── 10.2 docker-compose.yml
│   ├── 10.3 .dockerignore
│   ├── 10.4 Recolección de estáticos (WhiteNoise)
│   └── 10.5 Configuración producción (DEBUG=False)
│
└── 11.0 Pruebas
    ├── 11.1 Configuración (pytest.ini)
    ├── 11.2 Tests de modelos
    ├── 11.3 Tests de vistas
    ├── 11.4 Tests de acceso por roles
    └── 11.5 Tests de registro y autenticación
```

---

## 2. Cronograma del Proyecto

### 2.1 Diagrama de Gantt

| Fase | Actividad | Duración | Sem 1 | Sem 2 | Sem 3 | Sem 4 | Sem 5 | Sem 6 | Sem 7 | Sem 8 |
|------|-----------|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| **1** | Configuración del entorno | 2 días | ██ | | | | | | | |
| **2** | Productos: modelos y CRUD | 5 días | | █████ | | | | | | |
| **3** | Clientes: auth y perfiles | 5 días | | █████ | | | | | | |
| **4** | Pedidos: carrito y checkout | 7 días | | | ███████ | | | | | |
| **5** | Mercado Pago (pagos) | 4 días | | | | ████ | | | | |
| **6** | Inventario y proveedores | 5 días | | | | █████ | | | | |
| **7** | Dashboard y estadísticas | 3 días | | | | | ███ | | | |
| **8** | Frontend y diseño visual | 5 días | | | | | █████ | | | |
| **9** | Seguridad | 3 días | | | | | | ███ | | |
| **10** | Docker y despliegue | 3 días | | | | | | ███ | | |
| **11** | Pruebas | 4 días | | | | | | | ████ | |
| **12** | Documentación | 3 días | | | | | | | | ███ |

**Duración total estimada:** 8 semanas

### 2.2 Hitos

| Hito | Fecha estimada | Entregable |
|------|---------------|------------|
| H1 - Configuración lista | Día 2 | Proyecto Django funcionando con BD |
| H2 - Catálogo completo | Día 7 | CRUD de categorías y productos operativo |
| H3 - Autenticación funcional | Día 12 | Registro, login, perfiles, roles |
| H4 - Carrito y checkout | Día 19 | Flujo de compra completo sin pagos |
| H5 - Pagos integrados | Día 23 | Checkout con Mercado Pago |
| H6 - Inventario operativo | Día 28 | Movimientos, alertas, proveedores |
| H7 - Frontend finalizado | Día 33 | Diseño responsive, HTMX, Alpine.js |
| H8 - Seguridad implementada | Día 36 | RBAC, CSP, rate limiting |
| H9 - Docker listo | Día 39 | Contenedor funcionando |
| H10 - Pruebas superadas | Día 43 | Tests pasando |
| H11 - Documentación completa | Día 46 | README, C1, C2, C3 |

---

## 3. Recursos

### 3.1 Recursos Humanos

| Rol | Responsabilidades |
|-----|-------------------|
| Desarrollador Full Stack | Implementación de todos los módulos, frontend y backend |
| Diseñador UI/UX | Tema visual, experiencia de compra, responsive design |
| Tester | Pruebas funcionales, de seguridad y de integración |
| Administrador de infraestructura | Docker, despliegue, configuración producción |

### 3.2 Recursos Tecnológicos

| Recurso | Especificación | Propósito |
|---------|---------------|-----------|
| Python | 3.13+ | Lenguaje de programación |
| Django | 6.0.3 | Framework web |
| Visual Studio Code | Última versión | IDE de desarrollo |
| Git + GitHub | — | Control de versiones |
| Docker Desktop | Última versión | Contenedorización |
| SQLite | 3.x | Base de datos desarrollo |
| Mercado Pago | Cuenta test | Pasarela de pagos |
| Gmail | Cuenta email | Envío de correos |

### 3.3 Costos del Proyecto

| Concepto | Costo |
|----------|-------|
| Desarrollo (1 desarrollador x 8 semanas) | — |
| Docker Desktop | Gratuito |
| Python/Django | Open source |
| Mercado Pago | Comisión por transacción |
| Hosting (producción) | Variable |
| Dominio | Anual |
| **Total estimado** | **Open source + hosting** |

---

## 4. Arquitectura Técnica

### 4.1 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     Cliente (Navegador)                      │
│  Bootstrap 5 + HTMX + Alpine.js + Django Templates (HTML)   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Application Server                   │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ products │  │ customers│  │  orders  │  │ inventory  │  │
│  │  App     │  │  App     │  │  App     │  │  App       │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
│       │              │             │               │         │
│       └──────────────┴─────────────┴───────────────┘         │
│                          │                                    │
│                    ┌─────▼──────┐                            │
│                    │   ORM     │                             │
│                    │  Django   │                             │
│                    └─────┬──────┘                            │
└──────────────────────────┼──────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌─────────┐ ┌──────────┐ ┌────────┐
         │ SQLite  │ │ WhiteNoise│ │ Cache  │
         │  (DB)   │ │(Estáticos)│ │(Memoria)│
         └─────────┘ └──────────┘ └────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Mercado Pago │
                    │  (API ext.)  │
                    └──────────────┘
```

### 4.2 Diagrama de Navegación

```
                    ┌──────────────────┐
                    │   /tienda/       │
                    │   (Home público) │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │ /tienda/   │ │ /accounts/ │ │ /customers/│
      │ productos/ │ │ login/     │ │ register/  │
      └────────────┘ └────────────┘ └────────────┘
              │
              ▼
      ┌────────────────┐
      │ /tienda/       │
      │ productos/     │
      │ <slug>/        │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │ /orders/       │
      │ cart/          │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │ /orders/       │
      │ checkout/      │
      └────────┬───────┘
               │
         ┌─────┴──────┐
         ▼            ▼
  ┌──────────┐  ┌──────────┐
  │ Pago MP  │  │ Pago     │
  │ (externo)│  │ contra   │
  └──────────┘  │ entrega  │
                └──────────┘
         │            │
         └─────┬──────┘
               ▼
      ┌────────────────┐
      │ /orders/       │
      │ <pk>/          │
      │ (confirmación) │
      └────────────────┘


      ──── Panel Staff/Admin ────

               ┌──────────────┐
               │  / (Dashboard)│
               └──────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │products/ │ │categories│ │inventory/│
  │ CRUD     │ │ / CRUD   │ │Dashboard │
  └──────────┘ └──────────┘ └────┬─────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │movements/│ │suppliers/│ │ alerts/  │
              │ List +   │ │ CRUD     │ │ List +   │
              │ Create   │ │         │ │ Create   │
              └──────────┘ └──────────┘ └──────────┘

          ┌─────────────────────────────────────┐
          │ customers/        orders/            │
          │ Lista clientes    Lista pedidos      │
          │ Detalle cliente   Detalle pedido     │
          │                   Devoluciones       │
          └─────────────────────────────────────┘
```

### 4.3 Diagrama de Base de Datos (Relaciones)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────────┐                │
│  │ Category │1──N│ Product  │1──N│ ProductImage  │                │
│  └──────────┘     └────┬─────┘     └──────────────┘                │
│                        │                                            │
│          ┌─────────────┼─────────────┐                              │
│          ▼             ▼             ▼                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                        │
│  │ CartItem │   │OrderItem │   │Wishlist  │                        │
│  │(orders)  │   │(orders)  │   │(customers)│                       │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘                        │
│       │              │              │                              │
│  ┌────▼────┐    ┌────▼────┐    ┌────┴──────────┐                   │
│  │  Cart   │    │  Order  │    │  User (auth)  │                   │
│  │(orders) │    │(orders) │    │               │                   │
│  └─────────┘    └────┬────┘    │               │                   │
│                      │         │               │                   │
│                 ┌────▼────┐    │               │                   │
│                 │  Return │    │               │                   │
│                 │(orders) │    │               │                   │
│                 └─────────┘    │               │                   │
│                                │               │                   │
│         ┌──────────────────────┼───────────────┘                   │
│         │                      │                                   │
│         ▼                      ▼                                   │
│  ┌──────────────┐      ┌──────────────┐                            │
│  │   Profile    │      │   Address    │                            │
│  │ (customers)  │      │ (customers)  │                            │
│  └──────────────┘      └──────────────┘                            │
│                                                                     │
│  ┌──────────┐     ┌──────────────────┐     ┌──────────────────┐    │
│  │ Supplier │1──N│  StockMovement   │     │ InventoryAlert   │    │
│  │(inventory)│    │  (inventory)     │     │ (inventory)      │    │
│  └──────────┘     └────────┬─────────┘     └──────────────────┘    │
│                            │ (FK: Product)                         │
│                            ▼                                        │
│                      ┌──────────┐                                  │
│                      │ Product  │                                  │
│                      └──────────┘                                  │
│                                                                     │
│  ┌──────────┐                                                      │
│  │  Coupon  │ (independiente)                                       │
│  │(orders)  │                                                      │
│  └──────────┘                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Diseño de la Base de Datos

### 5.1 Diccionario de Datos

#### Tabla: `products_category`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| name | CharField | 100 | NOT NULL | Nombre de la categoría |
| slug | SlugField | 100 | UNIQUE, NOT NULL | Identificador para URLs |
| gender | CharField | 1 | NOT NULL, M/F/U/K | Género objetivo |
| description | TextField | — | NULL | Descripción |
| image | ImageField | — | NULL | Imagen representativa |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |

#### Tabla: `products_product`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| name | CharField | 200 | NOT NULL | Nombre del producto |
| slug | SlugField | 200 | UNIQUE, NOT NULL | Identificador para URLs |
| sku | CharField | 50 | UNIQUE, NOT NULL | Código interno |
| category_id | Integer | — | FK → Category, NOT NULL | Categoría |
| description | TextField | — | NULL | Descripción detallada |
| price | Decimal | 10,2 | NOT NULL | Precio original |
| discount_price | Decimal | 10,2 | NULL | Precio con descuento |
| main_image | ImageField | — | NULL | Imagen principal |
| sizes | CharField | 200 | NULL | Tallas (separadas por coma) |
| colors | CharField | 200 | NULL | Colores (separados por coma) |
| material | CharField | 100 | NULL | Material |
| stock_quantity | Integer | — | NOT NULL, ≥ 0 | Stock actual |
| status | CharField | 20 | NOT NULL, active/inactive/out_of_stock | Estado |
| is_featured | Boolean | — | NOT NULL, default=False | Destacado |
| weight | Decimal | 5,2 | NULL | Peso en kg |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |
| updated_at | DateTime | — | NOT NULL, Auto | Fecha de actualización |

#### Tabla: `products_productimage`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| product_id | Integer | — | FK → Product, NOT NULL | Producto asociado |
| image | ImageField | — | NOT NULL | Archivo de imagen |
| alt_text | CharField | 200 | NULL | Texto alternativo |
| order | Integer | — | NOT NULL, default=0 | Orden de visualización |

#### Tabla: `customers_profile`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| user_id | Integer | — | FK → User, UNIQUE, NOT NULL | Usuario asociado |
| phone | CharField | 20 | NULL | Teléfono |
| birth_date | Date | — | NULL | Fecha de nacimiento |
| avatar | ImageField | — | NULL | Foto de perfil |
| preferences | TextField | — | NULL | Preferencias de estilo |
| newsletter | Boolean | — | NOT NULL, default=True | Suscripción |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |

#### Tabla: `customers_address`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| user_id | Integer | — | FK → User, NOT NULL | Dueño |
| address_type | CharField | 20 | NOT NULL, shipping/billing | Tipo |
| name | CharField | 100 | NOT NULL | Nombre (Casa, Oficina) |
| street | CharField | 200 | NOT NULL | Calle y número |
| city | CharField | 100 | NOT NULL | Ciudad |
| state | CharField | 100 | NOT NULL | Estado/Provincia |
| zip_code | CharField | 20 | NOT NULL | Código postal |
| country | CharField | 100 | NOT NULL, default='México' | País |
| is_default | Boolean | — | NOT NULL, default=False | Dirección principal |
| phone | CharField | 20 | NULL | Teléfono de contacto |

#### Tabla: `customers_wishlist`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| user_id | Integer | — | FK → User, NOT NULL | Dueño |
| product_id | Integer | — | FK → Product, NOT NULL | Producto |
| added_at | DateTime | — | NOT NULL, Auto | Fecha de adición |
| notes | TextField | — | NULL | Notas |

**Unique:** (user_id, product_id)

#### Tabla: `orders_cart`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| user_id | Integer | — | FK → User, UNIQUE, NOT NULL | Dueño |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |
| updated_at | DateTime | — | NOT NULL, Auto | Fecha de actualización |

#### Tabla: `orders_cartitem`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| cart_id | Integer | — | FK → Cart, NOT NULL | Carrito |
| product_id | Integer | — | FK → Product, NOT NULL | Producto |
| quantity | Integer | — | NOT NULL, ≥ 1 | Cantidad |
| size | CharField | 10 | NULL | Talla seleccionada |
| color | CharField | 50 | NULL | Color seleccionado |
| added_at | DateTime | — | NOT NULL, Auto | Fecha de adición |

**Unique:** (cart_id, product_id, size, color)

#### Tabla: `orders_order`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| order_number | CharField | 20 | UNIQUE, NOT NULL | Número de orden (ANG1xxxx) |
| user_id | Integer | — | FK → User, NOT NULL | Cliente |
| status | CharField | 20 | NOT NULL, default='pending' | Estado del pedido |
| payment_status | CharField | 20 | NOT NULL, default='pending' | Estado del pago |
| shipping_address | TextField | — | NULL | Dirección de envío |
| billing_address | TextField | — | NULL | Dirección facturación |
| subtotal | Decimal | 10,2 | NOT NULL, default=0 | Subtotal |
| shipping_cost | Decimal | 10,2 | NOT NULL, default=0 | Costo de envío |
| tax | Decimal | 10,2 | NOT NULL, default=0 | Impuestos |
| discount | Decimal | 10,2 | NOT NULL, default=0 | Descuento |
| total | Decimal | 10,2 | NOT NULL, default=0 | Total |
| payment_method | CharField | 50 | NULL | Método de pago |
| transaction_id | CharField | 100 | NULL | ID de transacción |
| tracking_number | CharField | 100 | NULL | Número de rastreo |
| shipped_at | DateTime | — | NULL | Fecha de envío |
| delivered_at | DateTime | — | NULL | Fecha de entrega |
| customer_notes | TextField | — | NULL | Notas del cliente |
| internal_notes | TextField | — | NULL | Notas internas |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |
| updated_at | DateTime | — | NOT NULL, Auto | Fecha de actualización |

#### Tabla: `orders_orderitem`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| order_id | Integer | — | FK → Order, NOT NULL | Pedido |
| product_id | Integer | — | FK → Product, NOT NULL | Producto |
| quantity | Integer | — | NOT NULL | Cantidad |
| size | CharField | 10 | NULL | Talla |
| color | CharField | 50 | NULL | Color |
| unit_price | Decimal | 10,2 | NOT NULL | Precio unitario |
| total_price | Decimal | 10,2 | NOT NULL | Total (qty × unit_price) |

#### Tabla: `orders_coupon`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| code | CharField | 50 | UNIQUE, NOT NULL | Código del cupón |
| discount_type | CharField | 20 | NOT NULL, percentage/fixed | Tipo de descuento |
| discount_value | Decimal | 10,2 | NOT NULL | Valor del descuento |
| min_purchase | Decimal | 10,2 | NOT NULL, default=0 | Compra mínima |
| max_uses | Integer | — | NOT NULL, default=0 (ilimitado) | Usos máximos |
| used_count | Integer | — | NOT NULL, default=0 | Veces usado |
| is_active | Boolean | — | NOT NULL, default=True | Activo |
| valid_from | DateTime | — | NOT NULL | Inicio vigencia |
| valid_to | DateTime | — | NOT NULL | Fin vigencia |

#### Tabla: `orders_return`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| order_id | Integer | — | FK → Order, NOT NULL | Pedido |
| reason | CharField | 20 | NOT NULL | Razón (defective, wrong_item, etc.) |
| description | TextField | — | NULL | Descripción |
| status | CharField | 20 | NOT NULL, default='requested' | Estado |
| refund_amount | Decimal | 10,2 | NULL | Monto a reembolsar |
| admin_notes | TextField | — | NULL | Notas del admin |
| created_at | DateTime | — | NOT NULL, Auto | Fecha de creación |
| updated_at | DateTime | — | NOT NULL, Auto | Fecha de actualización |

#### Tabla: `inventory_supplier`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| name | CharField | 200 | NOT NULL | Nombre |
| contact_person | CharField | 100 | NULL | Contacto |
| email | EmailField | — | NULL | Correo |
| phone | CharField | 20 | NULL | Teléfono |
| address | TextField | — | NULL | Dirección |
| tax_id | CharField | 50 | NULL | RFC/NIT |
| is_active | Boolean | — | NOT NULL, default=True | Activo |

#### Tabla: `inventory_stockmovement`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| product_id | Integer | — | FK → Product, NOT NULL | Producto |
| movement_type | CharField | 20 | NOT NULL (in/out/adjustment/return) | Tipo |
| quantity | Integer | — | NOT NULL | Cantidad |
| unit_cost | Decimal | 10,2 | NULL | Costo unitario |
| total_cost | Decimal | 10,2 | NULL | Costo total |
| supplier_id | Integer | — | FK → Supplier, NULL | Proveedor |
| reference_number | CharField | 100 | NULL | Número de referencia |
| notes | TextField | — | NULL | Notas |
| created_by_id | Integer | — | FK → User, NOT NULL | Usuario que registró |

#### Tabla: `inventory_inventoryalert`

| Campo | Tipo | Longitud | Restricciones | Descripción |
|-------|------|----------|---------------|-------------|
| id | Integer | — | PK, Auto | Identificador único |
| product_id | Integer | — | FK → Product, NOT NULL | Producto |
| threshold | Integer | — | NOT NULL, default=10 | Umbral mínimo |
| is_active | Boolean | — | NOT NULL, default=True | Alerta activa |
| last_triggered | DateTime | — | NULL | Última vez activada |

---

## 6. Diseño de Interfaz de Usuario

### 6.1 Paleta de Colores

| Color | Código | Uso |
|-------|--------|-----|
| Fondo oscuro | `#1a1a2e` | Navbar, footer |
| Dorado | `#c9a962` | Acentos, botones, enlaces |
| Texto claro | `#ffffff` | Texto principal |
| Texto oscuro | `#2d2d2d` | Texto sobre fondos claros |
| Bootstrap primary | `#0d6efd` | Botones y elementos estándar |

### 6.2 Tipografía

- **Títulos:** Playfair Display (serif, elegancia)
- **Cuerpo:** Inter (sans-serif, legibilidad)

### 6.3 Componentes UI

| Componente | Framework | Comportamiento |
|------------|-----------|----------------|
| Navbar | Bootstrap 5 | Responsive, colapsable, dropdown de usuario |
| Tarjetas de producto | Bootstrap 5 | Grid responsive, hover effects |
| Modal/Cart | HTMX | Actualización asíncrona sin recarga |
| Selector talla/color | Alpine.js | Estado reactivo, sin recarga de página |
| Badge carrito | Alpine.js | Contador actualizado dinámicamente |
| Mensajes flash | Bootstrap + HTMX | Alertas dismissibles con swap OOB |
| Formularios | django-crispy-forms | Renderizado Bootstrap 5 automático |
| Tablas | Bootstrap 5 | Responsive, con paginación |

---

## 7. Estrategia de Pruebas

| Tipo | Herramienta | Alcance |
|------|-------------|---------|
| Unitarias | pytest + pytest-django | Modelos, formularios, validaciones |
| De integración | pytest + Client | Vistas, flujos (registro, login, carrito) |
| De seguridad | pytest | Acceso por roles (staff_required, admin_required) |
| Funcionales | Manual | Flujo completo de compra, CRUD |

---

## 8. Estrategia de Despliegue

### 8.1 Entornos

| Entorno | Propósito | URL |
|---------|-----------|-----|
| Desarrollo | Desarrollo local | `http://localhost:8000` |
| Docker | Entorno reproducible | `http://localhost:8000` |
| Producción | Despliegue en servidor | Por definir |

### 8.2 Pasos de Despliegue

1. Construir imagen Docker: `docker-compose build`
2. Ejecutar migraciones: `docker-compose run web python manage.py migrate`
3. Recolectar estáticos: `docker-compose run web python manage.py collectstatic --noinput`
4. Crear superusuario: `docker-compose run web python manage.py createsuperuser`
5. Iniciar servicio: `docker-compose up -d`
