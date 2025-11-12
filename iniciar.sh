#!/bin/bash

# Script de inicio rápido para CRM El Sabanero
# ============================================

echo "🛒 CRM Supermercado El Sabanero - Inicio Rápido"
echo "================================================"
echo ""

# Verificar si Django está instalado
if ! python -c "import django" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    echo ""
fi

# Verificar si existe la base de datos
if [ ! -f "db.sqlite3" ]; then
    echo "🗄️  Creando base de datos..."
    python manage.py migrate
    echo ""
    
    echo "👥 Creando datos de demostración..."
    python crear_datos_demo.py
    echo ""
fi

echo "🚀 Iniciando servidor de desarrollo..."
echo ""
echo "📋 CREDENCIALES DE ACCESO:"
echo "   Admin: usuario 'admin' / contraseña 'admin123'"
echo "   Clientes: usuarios 'juan', 'maria', 'carlos' / contraseña 'demo123'"
echo ""
echo "🌐 Accede a:"
echo "   - Aplicación: http://localhost:8000/"
echo "   - Admin Django: http://localhost:8000/admin/"
echo ""
echo "⏹️  Para detener: presiona CTRL+C"
echo "================================================"
echo ""

python manage.py runserver
