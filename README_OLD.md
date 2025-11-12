# CRM - SUPERMERCADO EL SABANERO MINIMARKET

Sistema de CRM (Customer Relationship Management) para gestión de clientes y programa de fidelización del Supermercado El Sabanero.

## 🚀 Características

- ✅ **Registro de facturas** y acumulación automática de puntos
- ✅ **Sistema de niveles**: Bronce (0-1,999), Plata (2,000-4,999), Oro (5,000+)
- ✅ **Ranking mensual** de mejores clientes
- ✅ **Campañas promocionales** con multiplicadores de puntos
- ✅ **Sistema de premios** y referidos
- ✅ **Panel de administración** completo

## 📋 Requisitos

- Python 3.8 o superior
- Django 4.2.7

## 🛠️ Instalación y Ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Aplicar migraciones

```bash
python manage.py migrate
```

### 3. Crear datos de demostración (opcional)

```bash
python crear_datos_demo.py
```

Esto creará:
- Superusuario admin (usuario: `admin`, contraseña: `admin123`)
- 3 clientes de prueba (usuarios: `juan`, `maria`, `carlos` - contraseña: `demo123`)
- Facturas y puntos de ejemplo
- Una campaña promocional activa

### 4. Iniciar el servidor

```bash
python manage.py runserver
```

El sistema estará disponible en: **http://localhost:8000/**

## 🔑 Credenciales de Acceso

### Administrador
- **Usuario:** admin
- **Contraseña:** admin123
- **Panel Admin:** http://localhost:8000/admin/

### Clientes de Prueba
- **Usuarios:** juan, maria, carlos
- **Contraseña:** demo123 (para todos)

## 📱 Funcionalidades por Rol

### Cliente
- Ver puntos acumulados y nivel actual
- Registrar nuevas facturas
- Ver historial de puntos
- Consultar ranking mensual
- Ver premios obtenidos

### Administrador
- Gestión completa de clientes
- Supervisión de facturas
- Crear y administrar campañas
- Asignar premios
- Ver estadísticas y reportes

## 💡 Reglas de Puntos

- **1 punto** por cada $1,000 en compras
- Los puntos se multiplican durante campañas activas
- Niveles:
  - 🥉 **Bronce**: 0 - 1,999 puntos
  - 🥈 **Plata**: 2,000 - 4,999 puntos
  - 🥇 **Oro**: 5,000+ puntos

## 📂 Estructura del Proyecto

```
CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET/
├── clientes/               # App principal
│   ├── models.py          # Modelos (Cliente, Factura, Punto, etc.)
│   ├── views.py           # Vistas del sistema
│   ├── urls.py            # Rutas de la app
│   ├── admin.py           # Configuración del admin
│   ├── utils.py           # Funciones auxiliares
│   └── templates/         # Plantillas HTML
├── crm_sabanero/          # Configuración del proyecto
│   ├── settings.py        # Configuración Django
│   └── urls.py            # URLs principales
├── manage.py              # Script de gestión Django
├── crear_datos_demo.py    # Script para datos de prueba
└── requirements.txt       # Dependencias del proyecto
```

## 🔧 Comandos Útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Crear nueva app
python manage.py startapp nombre_app

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# Ejecutar shell de Django
python manage.py shell

# Recolectar archivos estáticos (producción)
python manage.py collectstatic
```

## 📊 Modelos Principales

- **Cliente**: Perfil extendido del usuario con nivel y teléfono
- **Factura**: Registro de compras del cliente
- **Punto**: Puntos acumulados por el cliente
- **Campaña**: Promociones con multiplicadores de puntos
- **Premio**: Recompensas otorgadas a clientes
- **Referido**: Sistema de referencias entre clientes

## 🌐 URLs Principales

- `/` - Página de inicio
- `/mis-puntos/` - Ver puntos del cliente
- `/registrar-factura/` - Registrar nueva factura
- `/ranking/` - Ranking mensual
- `/admin/panel/` - Panel de administración personalizado
- `/admin/` - Admin de Django

## 🤝 Contribuir

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está desarrollado para uso interno del Supermercado El Sabanero.

---

**Desarrollado con ❤️ para Supermercado El Sabanero**
