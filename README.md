# CRM - SUPERMERCADO EL SABANERO MINIMARKET

Sistema de CRM (Customer Relationship Management) para el autoservicio Supermercado El Sabanero Minimarket. Sistema completo de gestión de relaciones con clientes que permite identificar, registrar y administrar clientes de manera fácil y eficiente.

## Características

### Gestión de Clientes
- ✅ Registro de nuevos clientes con información completa
- ✅ Búsqueda rápida de clientes por cédula
- ✅ Actualización de información de clientes
- ✅ Listado completo de todos los clientes
- ✅ Identificación única por cédula

### Sistema de Compras
- ✅ Registro detallado de compras
- ✅ Múltiples métodos de pago (Efectivo, Tarjeta, Transferencia)
- ✅ Historial completo de compras por cliente
- ✅ Detalle de productos en cada compra

### Programa de Lealtad
- ✅ Acumulación automática de puntos (1 punto por cada $1,000)
- ✅ Canje de puntos ($100 por punto)
- ✅ Historial de transacciones de puntos
- ✅ Seguimiento de puntos en tiempo real

### Reportes y Análisis
- ✅ Top clientes por volumen de compras
- ✅ Reportes de ventas por período
- ✅ Estadísticas de clientes únicos
- ✅ Análisis de promedio de compra

## Requisitos

- Python 3.6 o superior
- SQLite3 (incluido en Python)
- Sistema operativo: Windows, Linux, o macOS

## Instalación

1. Clone o descargue este repositorio:
```bash
git clone https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET.git
cd CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
```

2. No requiere instalación de dependencias adicionales (usa solo la biblioteca estándar de Python)

## Uso

### Iniciar el Sistema

Para iniciar el sistema CRM:

```bash
python3 crm.py
```

O en Windows:
```bash
python crm.py
```

### Generar Datos de Ejemplo

Para probar el sistema con datos de ejemplo:

```bash
python3 generate_sample_data.py
```

Esto creará:
- 10 clientes de ejemplo
- 50 compras distribuidas en los últimos 30 días
- Algunos canjes de puntos de ejemplo

### Menú Principal

El sistema presenta un menú interactivo con las siguientes opciones:

```
1.  Registrar Nuevo Cliente
2.  Buscar Cliente
3.  Ver Todos los Clientes
4.  Actualizar Información de Cliente
5.  Registrar Compra
6.  Ver Historial de Compras de Cliente
7.  Canjear Puntos de Lealtad
8.  Ver Historial de Puntos
9.  Top Clientes
10. Reporte de Ventas
0.  Salir
```

## Ejemplos de Uso

### Registrar un Cliente Nuevo

1. Seleccione opción `1` del menú
2. Ingrese los datos del cliente:
   - Cédula (obligatorio)
   - Nombre (obligatorio)
   - Apellido (obligatorio)
   - Teléfono (opcional)
   - Email (opcional)
   - Dirección (opcional)

### Registrar una Compra

1. Seleccione opción `5` del menú
2. Ingrese la cédula del cliente
3. Seleccione el método de pago
4. Agregue productos uno por uno:
   - Nombre del producto
   - Cantidad
   - Precio unitario
5. Escriba 'fin' cuando termine de agregar productos
6. Confirme la compra

Los puntos se acumulan automáticamente (1 punto por cada $1,000 gastados).

### Canjear Puntos

1. Seleccione opción `7` del menú
2. Ingrese la cédula del cliente
3. Ingrese la cantidad de puntos a canjear
4. Cada punto vale $100 de descuento
5. Confirme el canje

## Estructura de Archivos

```
CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET/
│
├── crm.py                    # Aplicación principal
├── database.py               # Módulo de base de datos
├── generate_sample_data.py   # Generador de datos de ejemplo
├── requirements.txt          # Dependencias (ninguna adicional)
├── .gitignore               # Archivos a ignorar en Git
├── README.md                # Este archivo
└── crm_sabanero.db          # Base de datos (se crea automáticamente)
```

## Base de Datos

El sistema utiliza SQLite3 y crea automáticamente las siguientes tablas:

- **customers**: Información de clientes
- **compras**: Registro de compras
- **items_compra**: Detalle de productos en cada compra
- **transacciones_puntos**: Historial de puntos ganados/canjeados

## Características Técnicas

- **Base de datos**: SQLite3 (sin servidor, archivo local)
- **Interfaz**: CLI (Command Line Interface)
- **Lenguaje**: Python 3
- **Arquitectura**: Modular (separación de lógica de base de datos y aplicación)
- **Transacciones**: Soporte completo para integridad de datos

## Seguridad

- Validación de cédula única para evitar duplicados
- Validación de puntos disponibles antes de canjear
- Transacciones atómicas para garantizar consistencia
- Campos opcionales y obligatorios bien definidos

## Soporte

Para preguntas o problemas, por favor abra un issue en GitHub.

## Licencia

Este proyecto es de código abierto para uso del Supermercado El Sabanero Minimarket.

## Autor

Desarrollado para Supermercado El Sabanero Minimarket

---

**¡Gracias por usar nuestro Sistema CRM!** 🛒
