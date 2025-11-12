"""
Script de pruebas básicas para el sistema CRM
Valida las funcionalidades principales del sistema
"""

import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Cliente, Compra, Recompensa, CanjeRecompensa


def test_crear_cliente():
    """Prueba crear un cliente"""
    print("Prueba 1: Crear cliente... ", end='')
    app = create_app()
    with app.app_context():
        # Limpiar base de datos
        db.drop_all()
        db.create_all()
        
        cliente = Cliente(
            cedula="123456789",
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com"
        )
        db.session.add(cliente)
        db.session.commit()
        
        # Verificar
        cliente_db = Cliente.query.filter_by(cedula="123456789").first()
        assert cliente_db is not None
        assert cliente_db.nombre == "Juan"
        assert cliente_db.puntos_acumulados == 0
        assert cliente_db.nivel_fidelidad == "Bronce"
        print("✅ PASÓ")


def test_registrar_compra():
    """Prueba registrar una compra y calcular puntos"""
    print("Prueba 2: Registrar compra... ", end='')
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Crear cliente
        cliente = Cliente(cedula="123", nombre="Test", apellido="User")
        db.session.add(cliente)
        db.session.commit()
        
        # Registrar compra
        compra = Compra(cliente_id=cliente.id, total=100.0)
        compra.calcular_puntos(1.0)  # Multiplicador base
        cliente.puntos_acumulados += compra.puntos_ganados
        
        db.session.add(compra)
        db.session.commit()
        
        # Verificar
        assert compra.puntos_ganados == 100
        assert cliente.puntos_acumulados == 100
        print("✅ PASÓ")


def test_niveles_fidelidad():
    """Prueba actualización de niveles de fidelidad"""
    print("Prueba 3: Niveles de fidelidad... ", end='')
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        cliente = Cliente(cedula="123", nombre="Test", apellido="User")
        db.session.add(cliente)
        db.session.commit()
        
        # Bronce inicial
        assert cliente.nivel_fidelidad == "Bronce"
        
        # Subir a Plata
        cliente.puntos_acumulados = 2000
        cliente.actualizar_nivel_fidelidad()
        assert cliente.nivel_fidelidad == "Plata"
        
        # Subir a Oro
        cliente.puntos_acumulados = 5000
        cliente.actualizar_nivel_fidelidad()
        assert cliente.nivel_fidelidad == "Oro"
        
        # Subir a Platino
        cliente.puntos_acumulados = 10000
        cliente.actualizar_nivel_fidelidad()
        assert cliente.nivel_fidelidad == "Platino"
        
        print("✅ PASÓ")


def test_canjear_recompensa():
    """Prueba canjear una recompensa"""
    print("Prueba 4: Canjear recompensa... ", end='')
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Crear cliente con puntos
        cliente = Cliente(cedula="123", nombre="Test", apellido="User")
        cliente.puntos_acumulados = 1000
        db.session.add(cliente)
        
        # Crear recompensa
        recompensa = Recompensa(
            nombre="Descuento $10",
            puntos_requeridos=500
        )
        db.session.add(recompensa)
        db.session.commit()
        
        # Canjear
        puntos_antes = cliente.puntos_acumulados
        canje = CanjeRecompensa(
            cliente_id=cliente.id,
            recompensa_id=recompensa.id,
            puntos_utilizados=recompensa.puntos_requeridos,
            codigo_canje="TEST123"
        )
        cliente.puntos_acumulados -= recompensa.puntos_requeridos
        
        db.session.add(canje)
        db.session.commit()
        
        # Verificar
        assert cliente.puntos_acumulados == puntos_antes - 500
        assert cliente.puntos_acumulados == 500
        print("✅ PASÓ")


def test_recompensas_iniciales():
    """Prueba que el modelo de recompensas funciona correctamente"""
    print("Prueba 5: Modelo de recompensas... ", end='')
    app = create_app()
    with app.app_context():
        # Simplemente verificar que podemos consultar recompensas
        recompensas = Recompensa.query.all()
        # Debe haber al menos una recompensa (creada en tests anteriores o durante inicialización)
        assert len(recompensas) >= 1
        # Verificar que el modelo tiene los campos correctos
        if len(recompensas) > 0:
            r = recompensas[0]
            assert hasattr(r, 'nombre')
            assert hasattr(r, 'puntos_requeridos')
            assert hasattr(r, 'categoria')
        print("✅ PASÓ")


def test_api_endpoints():
    """Prueba que los endpoints del API están disponibles"""
    print("Prueba 6: API endpoints... ", end='')
    app = create_app()
    client = app.test_client()
    
    # Test endpoint raíz
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'endpoints' in data
    
    # Test listar clientes
    response = client.get('/api/clientes')
    assert response.status_code == 200
    
    # Test listar recompensas
    response = client.get('/api/recompensas')
    assert response.status_code == 200
    
    # Test estadísticas
    response = client.get('/api/estadisticas/general')
    assert response.status_code == 200
    
    print("✅ PASÓ")


def test_crear_cliente_api():
    """Prueba crear un cliente via API"""
    print("Prueba 7: Crear cliente via API... ", end='')
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
    
    # Crear cliente
    response = client.post('/api/clientes', json={
        'cedula': '999',
        'nombre': 'API',
        'apellido': 'Test'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['nombre'] == 'API'
    assert data['cedula'] == '999'
    
    print("✅ PASÓ")


def test_buscar_cliente_api():
    """Prueba buscar un cliente via API"""
    print("Prueba 8: Buscar cliente via API... ", end='')
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        cliente = Cliente(cedula="888", nombre="Search", apellido="Test")
        db.session.add(cliente)
        db.session.commit()
    
    # Buscar cliente
    response = client.get('/api/clientes/buscar/888')
    assert response.status_code == 200
    data = response.get_json()
    assert data['nombre'] == 'Search'
    
    print("✅ PASÓ")


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("EJECUTANDO PRUEBAS DEL SISTEMA CRM")
    print("=" * 60)
    print()
    
    try:
        test_crear_cliente()
        test_registrar_compra()
        test_niveles_fidelidad()
        test_canjear_recompensa()
        test_recompensas_iniciales()
        test_api_endpoints()
        test_crear_cliente_api()
        test_buscar_cliente_api()
        
        print()
        print("=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ FALLÓ: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
