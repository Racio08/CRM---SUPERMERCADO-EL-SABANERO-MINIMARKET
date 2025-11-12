# 🛒 GUÍA DE INSTALACIÓN - CRM EL SABANERO MINIMARKET

## 📋 REQUISITOS DEL SISTEMA

### Windows, Mac o Linux
- **Python 3.8 o superior** (Recomendado: Python 3.12)
- **Navegador web** (Chrome, Firefox, Edge, Safari)
- **Conexión a Internet** (solo para la instalación inicial)

---

## 🚀 INSTALACIÓN RÁPIDA (3 PASOS)

### **Opción 1: Instalación Automática (Recomendada)**

#### 📥 **Paso 1: Descargar el proyecto**

**Desde GitHub:**
```bash
git clone https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET.git
cd CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
```

**O descargar ZIP:**
1. Ir a: https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
2. Clic en el botón verde "Code"
3. Seleccionar "Download ZIP"
4. Descomprimir en una carpeta

---

#### ⚙️ **Paso 2: Ejecutar instalador automático**

**En Windows:**
```cmd
instalar_windows.bat
```

**En Mac/Linux:**
```bash
chmod +x instalar_unix.sh
./instalar_unix.sh
```

---

#### ▶️ **Paso 3: Iniciar el sistema**

**En Windows:**
```cmd
iniciar.bat
```

**En Mac/Linux:**
```bash
./iniciar.sh
```

El sistema se abrirá automáticamente en tu navegador en: **http://localhost:8000/**

---

## 🔧 INSTALACIÓN MANUAL (Paso a Paso)

### **Paso 1: Instalar Python**

#### Windows:
1. Descargar Python desde: https://www.python.org/downloads/
2. **IMPORTANTE:** Marcar la casilla "Add Python to PATH" durante la instalación
3. Verificar instalación abriendo CMD y ejecutando:
   ```cmd
   python --version
   ```

#### Mac:
```bash
# Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.12
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

### **Paso 2: Descargar el proyecto**

```bash
# Opción A: Con Git
git clone https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET.git
cd CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET

# Opción B: Descargar y descomprimir ZIP manualmente
```

---

### **Paso 3: Crear entorno virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### **Paso 4: Instalar dependencias**

```bash
pip install -r requirements.txt
```

---

### **Paso 5: Configurar base de datos**

```bash
python manage.py migrate
```

---

### **Paso 6: Crear datos iniciales**

```bash
# Crear superusuario admin
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sabanero.com', 'admin123')
    print('Superusuario creado: admin / admin123')
"

# Crear datos de demostración (opcional)
python crear_datos_demo.py
```

---

### **Paso 7: Iniciar el servidor**

```bash
python manage.py runserver
```

El sistema estará disponible en: **http://localhost:8000/**

---

## 🔐 CREDENCIALES DE ACCESO

### Administrador:
- **Usuario:** admin
- **Contraseña:** admin123
- **URL Admin:** http://localhost:8000/admin/

### Clientes de Prueba:
- **Usuarios:** juan, maria, carlos
- **Contraseña:** demo123 (para todos)

---

## 📱 ACCESO AL SISTEMA

Una vez iniciado, podrás acceder a:

- **Página Principal:** http://localhost:8000/
- **Registro de Clientes:** http://localhost:8000/registro/
- **Admin Django:** http://localhost:8000/admin/
- **Catálogo de Premios:** http://localhost:8000/premios/
- **Sistema de Referidos:** http://localhost:8000/referidos/

---

## 🛠️ CONFIGURACIÓN ADICIONAL

### Cambiar Puerto (opcional)

Si el puerto 8000 está ocupado:
```bash
python manage.py runserver 8080
```

Luego acceder a: http://localhost:8080/

---

### Permitir Acceso desde Otras Computadoras

```bash
python manage.py runserver 0.0.0.0:8000
```

Luego acceder desde otra PC en la red usando:
```
http://[IP-DEL-SERVIDOR]:8000
```

Para ver tu IP:
- **Windows:** `ipconfig`
- **Mac/Linux:** `ifconfig` o `ip addr`

---

## 📊 FUNCIONALIDADES PRINCIPALES

✅ **Registro de Clientes** con datos completos
✅ **Sistema de Puntos** (1 punto por cada $1,000 en compras)
✅ **Niveles:** Bronce, Plata, Oro
✅ **Campañas Promocionales** con multiplicadores de puntos
✅ **Catálogo de 19 Premios** (desde 500 hasta 15,000 puntos)
✅ **Sistema de Referidos** con bonificaciones
✅ **Ranking Mensual** de clientes
✅ **Panel de Administración** completo

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Python no se reconoce"
**Solución:** Python no está en el PATH. Reinstalar Python marcando "Add to PATH"

### Error: "pip no se reconoce"
**Solución:**
```bash
python -m ensurepip --upgrade
```

### Error: "Puerto en uso"
**Solución:** Cambiar puerto o detener proceso que lo usa:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [NUMERO_PID] /F

# Mac/Linux
lsof -i :8000
kill -9 [PID]
```

### Error al instalar dependencias
**Solución:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Base de datos corrupta
**Solución:**
```bash
# Eliminar base de datos
rm db.sqlite3
rm -rf clientes/migrations/0*.py

# Recrear
python manage.py makemigrations clientes
python manage.py migrate
python crear_datos_demo.py
```

---

## 🔄 ACTUALIZACIÓN DEL SISTEMA

```bash
# Detener servidor (Ctrl+C)

# Actualizar código
git pull origin main

# Aplicar migraciones
python manage.py migrate

# Reiniciar servidor
python manage.py runserver
```

---

## 📦 BACKUP DE DATOS

### Exportar datos:
```bash
python manage.py dumpdata > backup.json
```

### Importar datos:
```bash
python manage.py loaddata backup.json
```

### Backup manual:
Simplemente copiar el archivo `db.sqlite3` a un lugar seguro.

---

## 🌐 DESPLIEGUE EN PRODUCCIÓN

Para uso en producción se recomienda:

1. **Hosting recomendado:**
   - PythonAnywhere (Gratis hasta cierto límite)
   - Heroku
   - DigitalOcean
   - AWS

2. **Base de datos:**
   - Cambiar de SQLite a PostgreSQL o MySQL

3. **Seguridad:**
   - Cambiar `SECRET_KEY` en `settings.py`
   - Configurar `ALLOWED_HOSTS`
   - Usar `DEBUG = False`
   - Configurar HTTPS

---

## 📞 SOPORTE

Para problemas o dudas:
- **Repositorio:** https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET
- **Issues:** https://github.com/Racio08/CRM---SUPERMERCADO-EL-SABANERO-MINIMARKET/issues

---

## 📄 LICENCIA

Este proyecto está bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

---

**¡Gracias por usar el CRM de EL SABANERO MINIMARKET! 🛒**
