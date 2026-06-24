# C1 — Análisis del Proyecto

## ANGELOW Store — Plataforma de Comercio Electrónico Premium

---

## 1. Identificación del Problema

### 1.1 Descripción del Problema

Las marcas de moda independientes y emergentes carecen de una plataforma digital integrada que les permita gestionar de manera eficiente su catálogo de productos, inventario, clientes y ventas en línea. Actualmente, muchos emprendedores de moda dependen de múltiples herramientas no conectadas (redes sociales para mostrar productos, mensajería para tomar pedidos, hojas de cálculo para controlar inventario) lo que genera:

- Duplicidad de esfuerzos en la gestión de información
- Errores en el control de stock
- Dificultad para escalar el negocio
- Experiencia de compra poco profesional para el cliente
- Falta de trazabilidad en pedidos y pagos

### 1.2 Árbol de Problemas

```
                        PÉRDIDA DE VENTAS
                        E INSATISFACCIÓN
                             |
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
  Stock desactualizado   Procesos manuales   Mala experiencia
  y pérdida de ventas    y lentos            de compra
        |                    |                    |
  ┌─────┼─────┐        ┌────┼────┐         ┌────┼────┐
  ▼     ▼     ▼        ▼    ▼    ▼         ▼    ▼    ▼
Sin   Sin   Control  Pedidos Pagos  Sin    Sin   Sin
siste- catá- de      por     no       carrito tienda pasarela
ma de logo stock     WhatsApp integrados        online de pago
stock  digital       /redes                    propio
```

---

## 2. Justificación del Proyecto

La industria de la moda en Colombia ha experimentado un crecimiento significativo en el comercio electrónico, con un aumento del 40% en ventas online en los últimos dos años. Sin embargo, muchas marcas pequeñas y medianas no tienen acceso a plataformas robustas y asequibles que se adapten a sus necesidades específicas.

**ANGELOW Store** surge como una solución integral que permite a una marca de moda premium:

1. **Digitalizar su catálogo** con imágenes, tallas, colores y descripciones detalladas
2. **Automatizar el控制 de inventario** con movimientos de stock y alertas
3. **Profesionalizar la experiencia de compra** con carrito, checkout y pagos en línea
4. **Gestionar clientes y pedidos** desde un panel administrativo unificado
5. **Escalar operaciones** sin incrementar proporcionalmente la carga operativa

---

## 3. Objetivos

### 3.1 Objetivo General

Desarrollar e implementar una plataforma de comercio electrónico para la marca ANGELOW que permita la gestión integral de productos, inventario, clientes, pedidos y pagos en línea, utilizando Django como framework principal y buenas prácticas de desarrollo de software.

### 3.2 Objetivos Específicos

1. **Diseñar e implementar un catálogo de productos** con categorización, galería de imágenes, tallas y colores, y precios con descuentos.

2. **Desarrollar un sistema de inventario** que registre movimientos de stock, gestione proveedores y genere alertas automáticas de stock bajo.

3. **Implementar un módulo de clientes** con registro, perfiles, direcciones múltiples y lista de deseos.

4. **Construir un flujo de compras completo** con carrito de compras, checkout, cupones de descuento y pasarela de pago (Mercado Pago).

5. **Diseñar un sistema de pedidos y devoluciones** con trazabilidad de estados, notificaciones por email y gestión administrativa.

6. **Implementar control de acceso basado en roles** (Admin, Staff, Cliente) con permisos granulares.

7. **Contenedorizar la aplicación** con Docker para facilitar el despliegue y la reproducción del entorno.

---

## 4. Alcance

### 4.1 Incluye

| Módulo | Funcionalidades |
|--------|----------------|
| Catálogo | CRUD de categorías y productos, galería de imágenes, filtros, búsqueda, destacados |
| Inventario | Movimientos de stock (entrada/salida/ajuste/devolución), proveedores, alertas de stock mínimo |
| Clientes | Registro, perfil, direcciones, wishlist, autenticación, recuperación de contraseña |
| Carrito | Agregar/actualizar/eliminar items, selección de talla y color, contador en navbar |
| Checkout | Dirección de envío, cupón de descuento, cálculo de impuestos y envío, pago MP o contra entrega |
| Pedidos | Creación, listado con filtros, detalle, actualización de estado, cancelación, email de confirmación |
| Devoluciones | Solicitud, aprobación, recepción, reembolso |
| Seguridad | RBAC (Admin/Staff/Cliente), CSRF, rate limiting, CSP, sesiones seguras |
| Infraestructura | Docker, WhiteNoise para estáticos, configuración de producción (SSL, HSTS) |

### 4.2 Excluye

- Aplicación móvil nativa
- Integración con redes sociales (login social)
- Módulo de facturación electrónica (DIAN)
- Múltiples monedas o idiomas
- Panel de analytics avanzado (más allá de estadísticas básicas)
- Integración con gateways de pago adicionales (solo Mercado Pago)

---

## 5. Requisitos del Sistema

### 5.1 Requisitos Funcionales

| ID | Requisito | Módulo |
|----|-----------|--------|
| RF-01 | El sistema debe permitir crear, editar, listar y eliminar categorías de productos | Catálogo |
| RF-02 | El sistema debe permitir crear, editar, listar y eliminar productos con imágenes múltiples | Catálogo |
| RF-03 | El sistema debe mostrar productos activos en la tienda pública con filtros | Catálogo |
| RF-04 | El sistema debe gestionar tallas y colores por producto | Catálogo |
| RF-05 | El sistema debe registrar movimientos de stock (entrada, salida, ajuste, devolución) | Inventario |
| RF-06 | El sistema debe gestionar proveedores (CRUD) | Inventario |
| RF-07 | El sistema debe generar alertas cuando el stock esté por debajo del umbral | Inventario |
| RF-08 | El sistema debe permitir el registro de nuevos clientes | Clientes |
| RF-09 | El sistema debe permitir a los clientes gestionar su perfil y direcciones | Clientes |
| RF-10 | El sistema debe permitir agregar productos a una lista de deseos | Clientes |
| RF-11 | El sistema debe autenticar usuarios mediante login/password | Clientes |
| RF-12 | El sistema debe permitir agregar productos al carrito con talla y color | Carrito |
| RF-13 | El sistema debe permitir modificar cantidades y eliminar items del carrito | Carrito |
| RF-14 | El sistema debe procesar el checkout con selección de dirección y método de pago | Pedidos |
| RF-15 | El sistema debe aplicar cupones de descuento en el checkout | Pedidos |
| RF-16 | El sistema debe crear pedidos con items, cálculos de subtotal, impuestos y total | Pedidos |
| RF-17 | El sistema debe integrarse con Mercado Pago para pagos en línea | Pedidos |
| RF-18 | El sistema debe permitir cancelar pedidos (solo pendientes) | Pedidos |
| RF-19 | El sistema debe gestionar devoluciones con flujo de estados | Pedidos |
| RF-20 | El sistema debe enviar email de confirmación de pedido | Pedidos |
| RF-21 | El sistema debe tener 3 roles: Admin, Staff, Cliente con diferentes permisos | Seguridad |
| RF-22 | El sistema debe redirigir al usuario según su rol después del login | Seguridad |
| RF-23 | El sistema debe mostrar un dashboard con estadísticas al Admin/Staff | Dashboard |

### 5.2 Requisitos No Funcionales

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-01 | Usabilidad | Interfaz responsive (Bootstrap 5), experiencia de compra fluida con HTMX |
| RNF-02 | Seguridad | CSRF, contraseñas validadas, rate limiting en login, CSP, cookies seguras |
| RNF-03 | Portabilidad | Contenedor Docker, dependencias fijas en requirements.txt |
| RNF-04 | Mantenibilidad | Arquitectura modular (4 apps Django), código documentado |
| RNF-05 | Rendimiento | WhiteNoise para estáticos, paginación en listados, LocMemCache |
| RNF-06 | Escalabilidad | Preparado para migrar a PostgreSQL, separación de entornos dev/prod |
| RNF-07 | Confiabilidad | Validaciones a nivel de modelo, formulario y vista; rollback de stock en cancelaciones |

---

## 6. Tecnologías Seleccionadas

| Componente | Tecnología | Versión | Razón |
|------------|------------|---------|-------|
| Backend | Django | 6.0.3 | Framework maduro, batteries-included, ORM potente |
| Base de datos | SQLite | 3.x | Simple, cero configuración, ideal para desarrollo |
| Frontend | Bootstrap 5 | 5.3.0 | Responsive, componentes listos, personalizable |
| AJAX | HTMX | 2.0.4 | Interacciones dinámicas sin JavaScript complejo |
| Estado cliente | Alpine.js | 3.14.8 | Reactividad liviana sin framework pesado |
| Pagos | Mercado Pago SDK | 3.2.0 | Líder en Latinoamérica, documentación en español |
| Estáticos | WhiteNoise | 6.12.0 | Servir estáticos sin servidor web adicional |
| Testing | pytest | 9.1.1 | Sintaxis concisa, potente, extensible |
| Contenedor | Docker | — | Entorno reproducible, despliegue simplificado |
| Formularios | django-crispy-forms | 2.6 | Renderizado consistente con Bootstrap 5 |

---

## 7. Roles de Usuario

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| Admin | Administrador del sistema | Acceso total al sistema, incluyendo Django Admin |
| Staff | Personal operativo | CRUD de productos, categorías, pedidos, inventario, clientes |
| Cliente | Comprador en la tienda | Catálogo, carrito, compras, perfil, pedidos propios |
| Anónimo | Visitante no registrado | Solo navegación del catálogo público |

---

## 8. Análisis de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Pérdida de datos en DB SQLite | Baja | Alto | Volumen Docker para persistencia, migración a PostgreSQL en producción |
| Falla en pasarela de pago | Media | Alto | Soporte para pago contra entrega como respaldo |
| Acceso no autorizado | Baja | Alto | RBAC, decoradores, validación en vistas |
| Bajo rendimiento con muchos productos | Baja | Medio | Paginación, índices en BD, caché |
| Error humano en operaciones de stock | Media | Medio | Validaciones, movimientos de ajuste, historial |
