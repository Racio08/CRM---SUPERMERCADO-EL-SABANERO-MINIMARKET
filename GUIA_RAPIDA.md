# Guía Rápida de Inicio - CRM Supermercado El Sabanero Minimarket

## Inicio Rápido en 3 Pasos

### Paso 1: Ejecutar el Sistema
```bash
python3 crm.py
```

### Paso 2: Generar Datos de Ejemplo (Opcional)
Si desea probar el sistema con datos de ejemplo primero:
```bash
python3 generate_sample_data.py
```

### Paso 3: ¡Empezar a Usar!
Seleccione las opciones del menú para gestionar clientes.

---

## Tareas Comunes

### Registrar un Nuevo Cliente
1. Opción `1` - Registrar Nuevo Cliente
2. Ingrese cédula, nombre, apellido
3. Opcionalmente: teléfono, email, dirección

### Registrar una Compra
1. Opción `5` - Registrar Compra
2. Ingrese cédula del cliente
3. Seleccione método de pago
4. Agregue productos (nombre, cantidad, precio)
5. Escriba 'fin' cuando termine
6. Los puntos se acumulan automáticamente

### Ver Clientes Top
1. Opción `9` - Top Clientes
2. Ingrese cantidad de clientes a mostrar
3. Ve lista ordenada por total gastado

### Canjear Puntos
1. Opción `7` - Canjear Puntos
2. Ingrese cédula del cliente
3. Ingrese puntos a canjear
4. Cada punto = $100 de descuento

---

## Programa de Lealtad

- **Ganar Puntos**: 1 punto por cada $1,000 gastados
- **Canjear Puntos**: 1 punto = $100 de descuento
- **Ejemplo**: Compra de $50,000 = 50 puntos ganados

---

## Métodos de Pago Disponibles

1. Efectivo
2. Tarjeta
3. Transferencia

---

## Reportes Disponibles

### Reporte de Ventas (Opción 10)
- Total de compras en período
- Total de ventas ($)
- Promedio por compra
- Clientes únicos

### Top Clientes (Opción 9)
- Ranking por total gastado
- Número de compras
- Puntos de lealtad

---

## Requisitos del Sistema

- Python 3.6 o superior (incluido en la mayoría de sistemas)
- No requiere instalación de paquetes adicionales
- Compatible con Windows, Linux, macOS

---

## Solución de Problemas

### Error: "command not found: python3"
- En Windows, use: `python crm.py`
- En Linux/Mac, use: `python3 crm.py`

### Error: No se puede abrir la base de datos
- Asegúrese de tener permisos de escritura en el directorio
- La base de datos se crea automáticamente en el primer uso

---

## Soporte

Para más información, consulte el archivo README.md completo.
