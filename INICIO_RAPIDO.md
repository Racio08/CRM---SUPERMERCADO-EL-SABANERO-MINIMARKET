# 🚀 Guía de Inicio Rápido - CRM Supermercado El Sabanero

## Instalación en 3 Pasos

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Iniciar el Servidor
```bash
python app.py
```

Verás un mensaje como este:
```
============================================================
CRM - SUPERMERCADO EL SABANERO MINIMARKET
Sistema de Identificación y Fidelización de Clientes
============================================================

Servidor iniciado en: http://localhost:5000
```

### Paso 3: Abrir la Interfaz Web
1. Abre el archivo `index.html` en tu navegador
2. ¡Listo! Ya puedes usar el sistema

## 📋 Primeros Pasos

### 1. Registrar tu Primer Cliente
1. Ve a la pestaña "Clientes"
2. Completa el formulario:
   - Cédula: 1234567890
   - Nombre: Juan
   - Apellido: Pérez
   - Email: juan@example.com
3. Haz clic en "Registrar Cliente"

### 2. Registrar una Compra
1. Ve a la pestaña "Compras"
2. Ingresa la cédula: 1234567890
3. Haz clic en "Verificar Cliente"
4. Ingresa el total: 100.00
5. Haz clic en "Registrar Compra"
6. ¡El cliente ganó 100 puntos!

### 3. Canjear una Recompensa
1. Ve a la pestaña "Recompensas"
2. Ingresa la cédula: 1234567890
3. Haz clic en "Ver Recompensas Disponibles"
4. Si tiene puntos suficientes, haz clic en "Canjear"

### 4. Ver Estadísticas
1. Ve a la pestaña "Estadísticas"
2. Verás un resumen completo del sistema

## 🎯 Conceptos Clave

### Sistema de Puntos
- 1 punto = $1 dólar gastado (base)
- Los puntos aumentan según el nivel del cliente

### Niveles de Fidelidad
- **Bronce** (0-1,999 pts): 1.0x puntos
- **Plata** (2,000-4,999 pts): 1.2x puntos
- **Oro** (5,000-9,999 pts): 1.5x puntos
- **Platino** (10,000+ pts): 2.0x puntos

### Recompensas Pre-Cargadas
El sistema viene con recompensas de ejemplo:
- Descuento $5 (500 puntos)
- Descuento $10 (1,000 puntos)
- Producto Gratis (2,000 puntos)
- Canasta Premium (5,000 puntos)

## 🧪 Probar con el Script de Ejemplo

```bash
# Asegúrate de que el servidor esté corriendo
python app.py

# En otra terminal, ejecuta:
python ejemplo_uso.py
```

Este script hará:
1. Registrar clientes de ejemplo
2. Realizar compras
3. Canjear recompensas
4. Mostrar estadísticas

## 📱 Usar la API Directamente

### Ejemplo con cURL:

```bash
# Registrar cliente
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"cedula":"123","nombre":"Test","apellido":"User"}'

# Registrar compra
curl -X POST http://localhost:5000/api/compras \
  -H "Content-Type: application/json" \
  -d '{"cliente_id":1,"total":100}'

# Ver estadísticas
curl http://localhost:5000/api/estadisticas/general
```

## ❓ Solución de Problemas

### El servidor no inicia
- Verifica que Python 3.8+ esté instalado: `python --version`
- Instala las dependencias: `pip install -r requirements.txt`

### No se conecta al API desde index.html
- Verifica que el servidor esté corriendo
- Abre la consola del navegador (F12) para ver errores
- Asegúrate de que la URL en index.html sea `http://localhost:5000/api`

### La interfaz no muestra datos
- Verifica que el servidor esté en `http://localhost:5000`
- Revisa la consola del navegador para errores CORS
- Intenta recargar la página (Ctrl+F5)

## 📚 Recursos Adicionales

- **README.md**: Documentación completa
- **ejemplo_uso.py**: Script de demostración
- **API Endpoints**: Ver en `http://localhost:5000/`

## 🎉 ¡Listo!

Ahora tienes un sistema completo de CRM para identificación y fidelización de clientes.

### Próximos Pasos Sugeridos:
1. Personalizar las recompensas
2. Crear promociones especiales
3. Integrar con tu sistema POS
4. Analizar las estadísticas

---

**¿Necesitas ayuda?** Consulta el README.md completo.
