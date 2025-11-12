# 📋 Guía de Gestión de Campañas Promocionales

## 🔐 Acceso al Panel de Administración

### Credenciales:
- **Usuario:** admin
- **Contraseña:** admin123
- **URL:** http://localhost:8000/admin/

---

## 🎯 Cómo Crear Campañas Promocionales

### Opción 1: Desde el Admin de Django

1. **Accede al admin:** http://localhost:8000/admin/
2. **Inicia sesión** con usuario `admin` y contraseña `admin123`
3. En la sección **CLIENTES**, haz clic en **Campanas**
4. Haz clic en **AÑADIR CAMPAÑA**
5. Completa los campos:
   - **Nombre:** Ej. "🎉 Black Friday 2025"
   - **Descripción:** Ej. "¡Puntos DOBLES en todas tus compras!"
   - **Fecha inicio:** Fecha de inicio de la campaña
   - **Fecha fin:** Fecha de finalización
   - **Multiplicador puntos:** Ej. 2.0 (puntos x2), 3.0 (puntos x3)
6. Haz clic en **GUARDAR**

### Opción 2: Panel Personalizado (Futuro)

Accede a: http://localhost:8000/panel/
Desde aquí podrás ver y gestionar campañas (requiere permisos de staff)

---

## 💡 Ideas de Campañas para Motivar Clientes

### 1️⃣ Campañas Estacionales
```
🎄 Navidad - Puntos x3 (Diciembre)
💝 Día de las Madres - Puntos x2.5 (Mayo)
🎃 Halloween - Puntos x2 (Octubre)
🎆 Año Nuevo - Puntos x2.5 (Enero)
```

### 2️⃣ Campañas de Fin de Semana
```
🌟 Fin de Semana Dorado - Puntos x2 (Viernes a Domingo)
🛒 Lunes de Ahorro - Puntos x1.5 (Cada lunes)
```

### 3️⃣ Campañas Flash
```
⚡ Flash 24 Horas - Puntos x4 (Un día específico)
🔥 Happy Hour - Puntos x3 (Ciertas horas del día)
```

### 4️⃣ Campañas por Aniversario
```
🎂 Aniversario El Sabanero - Puntos x5 (Fecha aniversario)
🎁 Cumpleaños del Cliente - Puntos x2 (En su cumpleaños)
```

---

## 📊 Cómo Funcionan las Campañas

### Multiplicadores:
- **x1.5** = Cliente gana 50% más puntos
- **x2.0** = Cliente gana el DOBLE de puntos
- **x3.0** = Cliente gana el TRIPLE de puntos
- **x5.0** = Cliente gana 5 VECES los puntos

### Ejemplo:
```
Compra: $50,000
Puntos normales: 50 puntos (1 punto por cada $1,000)
Con campaña x2: 100 puntos
Con campaña x3: 150 puntos
```

---

## 🎨 Visualización en la Página de Inicio

Las campañas aparecen automáticamente en http://localhost:8000/:

- **Campañas Activas:** Fondo morado degradado, destacadas arriba
- **Próximas Campañas:** Fondo rosa degradado, para generar expectativa

Los clientes verán:
- Nombre de la campaña con emoji
- Descripción motivacional
- Fechas de vigencia
- Multiplicador de puntos

---

## ✅ Campañas Actuales Creadas

1. **🎉 Black Friday 2025**
   - Multiplicador: x2.0
   - Vigencia: 12/11/2025 al 19/11/2025

2. **🎄 Navidad 2025**
   - Multiplicador: x3.0
   - Vigencia: 12/12/2025 al 27/12/2025

3. **💝 Día de las Madres**
   - Multiplicador: x2.5
   - Vigencia: 01/05/2025 al 31/05/2025

---

## 🚀 Tips para Motivar Clientes

1. **Usa emojis llamativos** en los nombres de campañas
2. **Mensajes motivacionales** en las descripciones
3. **Multiplicadores altos** en fechas especiales (x3, x4, x5)
4. **Campañas cortas** (3-7 días) crean urgencia
5. **Anuncia próximas campañas** para generar expectativa
6. **Combina con premios** (configurable en el admin)

---

## 📱 Accesos Rápidos

- **Admin:** http://localhost:8000/admin/
- **Gestión de Campañas:** http://localhost:8000/admin/clientes/campana/
- **Panel Personalizado:** http://localhost:8000/panel/
- **Página Pública:** http://localhost:8000/

---

**Nota:** Recuerda que los clientes verán las campañas activas automáticamente cuando ingresen al sistema, motivándolos a registrar sus facturas durante estos períodos especiales.
