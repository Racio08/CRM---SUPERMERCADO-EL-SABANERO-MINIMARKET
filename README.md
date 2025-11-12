# 🛒 CRM EL SABANERO MINIMARKET

Sistema de Gestión de Relación con Clientes (CRM) completo con programa de fidelización, premios y referidos.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2.7-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🚀 INICIO RÁPIDO

### Instalación Automática (3 pasos)

1. **Descargar el proyecto:**
   ```bash
   git clone https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET.git
   cd CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
   ```

2. **Instalar (ejecutar según tu sistema operativo):**
   ```bash
   # Windows
   instalar_windows.bat
   
   # Mac/Linux
   chmod +x instalar_unix.sh
   ./instalar_unix.sh
   ```

3. **Iniciar el sistema:**
   ```bash
   # Windows
   iniciar_windows.bat
   
   # Mac/Linux
   ./iniciar.sh
   ```

**¡Listo!** El sistema se abrirá automáticamente en tu navegador.

---

## 📖 DOCUMENTACIÓN COMPLETA

- 📘 **[Guía de Instalación Completa](INSTALACION.md)** - Instalación paso a paso
- 🎯 **[Guía de Campañas](GUIA_CAMPANAS.md)** - Cómo crear y gestionar campañas promocionales
- 🎁 **[Sistema de Premios y Referidos](SISTEMA_PREMIOS_REFERIDOS.md)** - Catálogo de premios y bonificaciones

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### 👥 Gestión de Clientes
- ✅ Registro completo de clientes con documento, dirección, contacto
- ✅ Sistema de niveles: Bronce, Plata, Oro
- ✅ Validación de datos y verificación de duplicados
- ✅ Perfiles personalizados con preferencias

### 💰 Sistema de Puntos
- ✅ **1 punto por cada $1,000** en compras
- ✅ Registro de facturas con validación
- ✅ Historial completo de puntos
- ✅ Cálculo automático de niveles

### 🎉 Campañas Promocionales
- ✅ **Multiplicadores de puntos** (x2, x3, x4, x5)
- ✅ Campañas con fechas de inicio y fin
- ✅ Visualización destacada en página principal
- ✅ **4 campañas pre-configuradas:**
  - 🎉 Black Friday (x2 puntos)
  - 🎄 Navidad (x3 puntos)
  - 💝 Día de las Madres (x2.5 puntos)

### 🎁 Catálogo de Premios
- ✅ **19 premios** organizados por niveles
- ✅ Desde **500 puntos** (combos dulces) hasta **15,000 puntos** (electrodomésticos)
- ✅ Control de stock y disponibilidad
- ✅ Indicadores visuales de premios alcanzables
- ✅ Premios destacados:
  - 🍫 Combos y productos básicos (500-1,500 pts)
  - 🎧 Tecnología y bonos (2,000-4,500 pts)
  - 📱 Smartphones, tablets, TV (5,000-15,000 pts)

### 🔗 Sistema de Referidos
- ✅ Código único de referido para cada cliente
- ✅ **500 puntos** por cada amigo referido
- ✅ **200 puntos** de bienvenida para nuevos clientes
- ✅ **Bonos especiales:**
  - 5 referidos: +1,000 puntos
  - 10 referidos: +2,500 puntos
  - 20 referidos: +5,000 puntos
- ✅ Botón para copiar y compartir código
- ✅ Seguimiento de referidos activos

### 📊 Reporting y Analytics
- ✅ Ranking mensual de clientes
- ✅ Panel de administración completo
- ✅ Estadísticas de puntos y facturas
- ✅ Historial de transacciones

### 🎨 Interfaz de Usuario
- ✅ Diseño responsivo y moderno
- ✅ Visualización de contraseñas con ícono de ojo
- ✅ Mensajes de confirmación y errores
- ✅ Navegación intuitiva
- ✅ Colores distintivos por nivel

---

## 🔐 ACCESO AL SISTEMA

### Credenciales por Defecto

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`
- URL: http://localhost:8000/admin/

**Clientes de Prueba:**
- Usuarios: `juan`, `maria`, `carlos`
- Contraseña: `demo123` (todos)

---

## 🌐 URLs del Sistema

| Descripción | URL |
|-------------|-----|
| Página Principal | http://localhost:8000/ |
| Registro de Clientes | http://localhost:8000/registro/ |
| Mis Puntos | http://localhost:8000/mis-puntos/ |
| Registrar Factura | http://localhost:8000/registrar-factura/ |
| Catálogo de Premios | http://localhost:8000/premios/ |
| Mis Referidos | http://localhost:8000/referidos/ |
| Ranking Mensual | http://localhost:8000/ranking/ |
| Panel Admin | http://localhost:8000/admin/ |

---

## 🛠️ TECNOLOGÍAS UTILIZADAS

- **Backend:** Django 4.2.7
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción recomendada)
- **Frontend:** HTML5, CSS3, JavaScript
- **Python:** 3.8+

---

## 📦 ESTRUCTURA DEL PROYECTO

```
CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET/
├── clientes/                    # App principal
│   ├── models.py               # Modelos (Cliente, Factura, Punto, etc.)
│   ├── views.py                # Vistas y lógica de negocio
│   ├── forms.py                # Formularios de registro
│   ├── admin.py                # Configuración del admin
│   ├── templates/              # Plantillas HTML
│   │   ├── clientes/
│   │   └── admin/
│   └── migrations/             # Migraciones de base de datos
├── crm_sabanero/               # Configuración del proyecto
│   ├── settings.py             # Configuración Django
│   └── urls.py                 # URLs principales
├── manage.py                   # Utilidad Django
├── requirements.txt            # Dependencias Python
├── db.sqlite3                  # Base de datos (creada al migrar)
├── instalar_windows.bat        # Instalador Windows
├── instalar_unix.sh            # Instalador Mac/Linux
├── iniciar_windows.bat         # Iniciador Windows
├── iniciar.sh                  # Iniciador Mac/Linux
├── crear_datos_demo.py         # Script para datos de prueba
├── INSTALACION.md              # Guía de instalación
├── GUIA_CAMPANAS.md            # Guía de campañas
└── SISTEMA_PREMIOS_REFERIDOS.md # Guía de premios
```

---

## 🆘 SOPORTE

¿Problemas con la instalación o uso?

1. **Consulta la documentación:**
   - [Guía de Instalación](INSTALACION.md)
   - [Solución de Problemas](INSTALACION.md#-solución-de-problemas)

2. **Reporta un problema:**
   - [Crear Issue en GitHub](https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET/issues)

---

## 📄 LICENCIA

Este proyecto está bajo la Licencia MIT.

---

## 👨‍💻 DESARROLLADO POR

**Racio08**
- GitHub: [@Racio08](https://github.com/Racio08)
- Repositorio: [CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET](https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET)

---

**¡Gracias por usar el CRM de EL SABANERO MINIMARKET! 🛒**

*Última actualización: Noviembre 2025*
