#!/usr/bin/env python
"""Script para crear datos iniciales de demostración"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_sabanero.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Cliente, Factura, Punto, Campana

# Crear superusuario admin
print("Creando superusuario admin...")
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@sabanero.com', '')
    admin.set_unusable_password()
    admin.save()
    print("✓ Superusuario 'admin' creado (sin contraseña)")
else:
    admin = User.objects.get(username='admin')
    print("✓ Superusuario 'admin' ya existe")

# Crear usuarios de prueba
print("\nCreando clientes de prueba...")
usuarios_prueba = [
    ('juan', 'Juan', 'Pérez', '3001234567', '1052345678'),
    ('maria', 'María', 'García', '3009876543', '1098765432'),
    ('carlos', 'Carlos', 'López', '3005551234', '1055512345'),
]

for username, first_name, last_name, telefono, numero_doc in usuarios_prueba:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=f'{username}@example.com'
        )
        user.set_unusable_password()
        user.save()
        Cliente.objects.create(
            user=user,
            telefono=telefono,
            numero_documento=numero_doc,
            direccion=f'Calle {numero_doc[-2:]} # 10-20',
            ciudad='Bogotá'
        )
        print(f"✓ Cliente {first_name} {last_name} creado (usuario: {username}, sin contraseña)")
    else:
        print(f"✓ Cliente {username} ya existe")

# Crear campaña de ejemplo
print("\nCreando campaña promocional...")
hoy = date.today()
if not Campana.objects.filter(nombre='Black Friday 2025').exists():
    Campana.objects.create(
        nombre='Black Friday 2025',
        descripcion='Puntos dobles en todas tus compras',
        fecha_inicio=hoy - timedelta(days=5),
        fecha_fin=hoy + timedelta(days=25),
        multiplicador_puntos=2.0
    )
    print("✓ Campaña 'Black Friday 2025' creada (puntos x2)")
else:
    print("✓ Campaña ya existe")

# Crear facturas de ejemplo
print("\nCreando facturas de ejemplo...")
juan_cliente = Cliente.objects.get(user__username='juan')
maria_cliente = Cliente.objects.get(user__username='maria')

facturas_ejemplo = [
    (juan_cliente, 'FAC-001', hoy - timedelta(days=10), 45000, 'Principal'),
    (juan_cliente, 'FAC-002', hoy - timedelta(days=5), 78000, 'Norte'),
    (maria_cliente, 'FAC-003', hoy - timedelta(days=8), 120000, 'Centro'),
    (maria_cliente, 'FAC-004', hoy - timedelta(days=2), 56000, 'Principal'),
]

for cliente, num, fecha, valor, sucursal in facturas_ejemplo:
    if not Factura.objects.filter(numero_factura=num).exists():
        factura = Factura.objects.create(
            cliente=cliente,
            numero_factura=num,
            fecha_compra=fecha,
            valor_total=valor,
            sucursal=sucursal,
            registrada=True
        )
        puntos = int(valor // 1000)
        Punto.objects.create(
            cliente=cliente,
            factura=factura,
            puntos_obtenidos=puntos,
            tipo='Compra'
        )
        print(f"✓ Factura {num} creada: ${valor:,} = {puntos} puntos")
    else:
        print(f"✓ Factura {num} ya existe")

# Actualizar niveles
print("\nActualizando niveles de clientes...")
from clientes.utils import calcular_nivel
for cliente in Cliente.objects.all():
    total = calcular_nivel(cliente)
    print(f"✓ {cliente.user.username}: {total} puntos - Nivel {cliente.nivel}")

print("\n" + "="*60)
print("✅ DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE")
print("="*60)
print("\n📋 USUARIOS CREADOS:")
print("-" * 60)
print("ADMINISTRADOR: admin (sin contraseña)")
print("CLIENTES: juan, maria, carlos (sin contraseña)")
print("\nNOTA: Los usuarios no tienen contraseña establecida.")
print("      Deben registrarla al primer ingreso.")
print("-" * 60)
