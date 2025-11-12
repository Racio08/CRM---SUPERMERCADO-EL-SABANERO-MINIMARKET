#!/usr/bin/env python
"""Script para crear perfil de cliente al usuario admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_sabanero.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Cliente

# Obtener usuario admin
admin = User.objects.get(username='admin')

# Verificar si tiene perfil de cliente
if not hasattr(admin, 'cliente'):
    Cliente.objects.create(
        user=admin,
        telefono='3001111111',
        nivel='Oro',
        numero_documento='1000000001',
        direccion='Oficina Principal',
        ciudad='Bogotá'
    )
    print(f"✓ Perfil de cliente creado para {admin.username}")
else:
    print(f"✓ {admin.username} ya tiene perfil de cliente")

# Verificar todos los usuarios sin perfil de cliente
usuarios_sin_cliente = User.objects.filter(cliente__isnull=True)
for i, user in enumerate(usuarios_sin_cliente, start=2):
    Cliente.objects.create(
        user=user,
        telefono='3000000000',
        nivel='Bronce',
        numero_documento=f'100000000{i}',
        direccion='Sin especificar',
        ciudad='Bogotá'
    )
    print(f"✓ Perfil de cliente creado para {user.username}")

print("\n✅ Todos los usuarios tienen perfil de cliente ahora")
