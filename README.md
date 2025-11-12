# 🏪 CRM - SUPERMERCADO EL SABANERO MINIMARKET

Sistema innovador de **Identificación y Fidelización de Clientes** para autoservicio.

## 🎯 Características Principales

### 1. Sistema de Identificación de Clientes
- **Registro rápido y sencillo** de clientes con cédula única
- Búsqueda instantánea por número de cédula
- Perfil completo del cliente (nombre, email, teléfono, dirección)
- Estado de cuenta en tiempo real

### 2. Programa de Fidelización Multinivel
El sistema incluye **4 niveles de fidelidad** con beneficios progresivos:

| Nivel | Puntos Requeridos | Multiplicador | Beneficios |
|-------|-------------------|---------------|------------|
| 🥉 **Bronce** | 0 - 1,999 | 1.0x | Acceso a recompensas básicas |
| 🥈 **Plata** | 2,000 - 4,999 | 1.2x | 20% más puntos por compra |
| 🥇 **Oro** | 5,000 - 9,999 | 1.5x | 50% más puntos por compra |
| 💎 **Platino** | 10,000+ | 2.0x | Doble puntos por compra |

### 3. Sistema de Puntos
- **1 punto por cada dólar gastado** (monto base)
- Multiplicadores según nivel de fidelidad
- Promociones especiales con puntos dobles o triples
- Acumulación automática en cada compra

### 4. Catálogo de Recompensas
- Descuentos en efectivo ($5, $10, $20+)
- Productos gratis de línea premium
- Canastas de productos especiales
- Servicios exclusivos

### 5. Gestión de Compras
- Registro de compras con número de factura
- Asignación automática de puntos
- Historial completo de transacciones
- Reportes por cliente

### 6. Campañas Promocionales
- Promociones con duración definida
- Multiplicadores de puntos temporales
- Segmentación por nivel de cliente
- Activación/desactivación flexible

### 7. Dashboard de Estadísticas
- Total de clientes activos
- Volumen de ventas
- Recompensas canjeadas
- Distribución de clientes por nivel
- Top 10 clientes más fieles

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET.git
cd CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Iniciar el servidor**
```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

5. **Abrir la interfaz web**
Abrir el archivo `index.html` en un navegador web moderno.

## 📖 Uso del Sistema

### Registrar un Cliente
1. Ir a la pestaña **"Clientes"**
2. Completar el formulario con los datos del cliente
3. Los campos obligatorios son: Cédula, Nombre y Apellido
4. Click en **"Registrar Cliente"**

### Registrar una Compra
1. Ir a la pestaña **"Compras"**
2. Ingresar la cédula del cliente
3. Click en **"Verificar Cliente"** para confirmar
4. Ingresar el monto total de la compra
5. Opcionalmente agregar número de factura y descripción
6. Click en **"Registrar Compra"**
7. Los puntos se asignan automáticamente según el nivel del cliente

### Canjear Recompensas
1. Ir a la pestaña **"Recompensas"**
2. Ingresar la cédula del cliente
3. Click en **"Ver Recompensas Disponibles"**
4. Seleccionar la recompensa deseada
5. Click en **"Canjear"**
6. Se genera un código único de canje

### Ver Estadísticas
1. Ir a la pestaña **"Estadísticas"**
2. Ver métricas generales del negocio
3. Revisar distribución de clientes por nivel
4. Consultar el Top 10 de clientes más fieles

## 🔌 API REST

El sistema incluye una API RESTful completa para integración con sistemas POS.

### Endpoints Principales

#### Clientes
```
GET    /api/clientes                    - Listar todos los clientes
POST   /api/clientes                    - Registrar nuevo cliente
GET    /api/clientes/{id}               - Obtener cliente por ID
GET    /api/clientes/buscar/{cedula}    - Buscar por cédula
PUT    /api/clientes/{id}               - Actualizar cliente
```

#### Compras
```
POST   /api/compras                     - Registrar compra
GET    /api/clientes/{id}/compras       - Historial de compras
```

#### Recompensas
```
GET    /api/recompensas                           - Listar recompensas
POST   /api/recompensas                           - Crear recompensa
GET    /api/clientes/{id}/recompensas-disponibles - Recompensas canjeables
POST   /api/canje                                 - Canjear recompensa
GET    /api/clientes/{id}/canjes                  - Historial de canjes
```

#### Promociones
```
GET    /api/promociones                 - Listar promociones activas
POST   /api/promociones                 - Crear promoción
```

#### Estadísticas
```
GET    /api/estadisticas/general        - Estadísticas generales
GET    /api/estadisticas/clientes/top   - Top clientes
```

### Ejemplo de Uso de la API

**Registrar un cliente:**
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cedula": "1234567890",
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234"
  }'
```

**Registrar una compra:**
```bash
curl -X POST http://localhost:5000/api/compras \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "total": 150.50,
    "numero_factura": "FAC-12345"
  }'
```

## 💡 Características Innovadoras

### 1. Sistema de Niveles Automático
El cliente avanza automáticamente de nivel al alcanzar los puntos necesarios, sin intervención manual.

### 2. Multiplicadores Inteligentes
Los puntos se calculan considerando:
- Nivel actual del cliente
- Promociones activas
- Multiplicadores especiales

### 3. Recompensas Segmentadas
Cada recompensa tiene un nivel mínimo requerido, creando incentivos para que los clientes mejoren su nivel.

### 4. Códigos de Canje Únicos
Cada canje genera un código alfanumérico único para control y verificación.

### 5. Gestión de Stock
Las recompensas pueden tener stock limitado o ilimitado, permitiendo controlar la disponibilidad.

### 6. Dashboard en Tiempo Real
Todas las estadísticas se actualizan automáticamente con cada transacción.

## 🎨 Interfaz de Usuario

La interfaz web incluye:
- ✅ Diseño moderno y responsive
- ✅ Navegación por pestañas intuitiva
- ✅ Colores distintivos por nivel de fidelidad
- ✅ Formularios validados
- ✅ Mensajes de confirmación
- ✅ Tablas ordenadas y buscables
- ✅ Tarjetas de recompensas visualmente atractivas
- ✅ Dashboard con métricas clave

## 🗄️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas:

- **clientes** - Información de clientes
- **compras** - Registro de transacciones
- **recompensas** - Catálogo de premios
- **canjes_recompensas** - Historial de canjes
- **promociones** - Campañas activas

La base de datos se crea automáticamente al iniciar la aplicación.

## 🔒 Seguridad

- Validación de datos en formularios
- Verificación de unicidad de cédulas
- Prevención de canjes duplicados
- Control de stock en recompensas
- Validación de puntos suficientes

## 📊 Casos de Uso

### Escenario 1: Cliente Nuevo
1. Cliente llega al supermercado
2. Se registra con cédula y datos básicos
3. Inicia en nivel Bronce con 0 puntos
4. Realiza su primera compra y gana puntos

### Escenario 2: Cliente Frecuente
1. Cliente identificado por cédula
2. Realiza compra de $100
3. Sistema calcula puntos según su nivel (ej: Oro = 150 puntos)
4. Si hay promoción activa, puntos se duplican (300 puntos)
5. Acumula puntos para próximo nivel

### Escenario 3: Canje de Recompensa
1. Cliente consulta recompensas disponibles
2. Sistema muestra solo las que puede canjear
3. Cliente selecciona descuento de $10 (1000 puntos)
4. Sistema genera código de canje único
5. Puntos se descuentan automáticamente

## 🔧 Personalización

El sistema es fácilmente personalizable:

- **Niveles de fidelidad**: Modificar umbrales y multiplicadores en `models.py`
- **Recompensas**: Agregar/modificar a través de la API o base de datos
- **Interfaz**: Personalizar colores y estilos en `index.html`
- **Cálculo de puntos**: Ajustar fórmula en `app.py`

## 📝 Licencia

Este proyecto está disponible para uso del Supermercado El Sabanero Minimarket.

## 👥 Soporte

Para preguntas o soporte, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para SUPERMERCADO EL SABANERO MINIMARKET**
