"""
Script de ejemplo para demostrar el uso del API del CRM
Este script muestra cómo interactuar con el sistema programáticamente
"""

import requests
import json
from datetime import datetime

# URL base del API
API_URL = "http://localhost:5000/api"


def print_section(title):
    """Imprime un encabezado de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def registrar_cliente(cedula, nombre, apellido, email=None, telefono=None):
    """Registra un nuevo cliente"""
    datos = {
        "cedula": cedula,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono
    }
    
    response = requests.post(f"{API_URL}/clientes", json=datos)
    
    if response.status_code == 201:
        cliente = response.json()
        print(f"✅ Cliente registrado: {cliente['nombre']} {cliente['apellido']}")
        print(f"   Cédula: {cliente['cedula']}")
        print(f"   ID: {cliente['id']}")
        return cliente
    else:
        print(f"❌ Error: {response.json().get('error', 'Error desconocido')}")
        return None


def buscar_cliente(cedula):
    """Busca un cliente por cédula"""
    response = requests.get(f"{API_URL}/clientes/buscar/{cedula}")
    
    if response.status_code == 200:
        cliente = response.json()
        print(f"Cliente encontrado:")
        print(f"  Nombre: {cliente['nombre']} {cliente['apellido']}")
        print(f"  Puntos: {cliente['puntos_acumulados']}")
        print(f"  Nivel: {cliente['nivel_fidelidad']}")
        return cliente
    else:
        print(f"❌ Cliente no encontrado")
        return None


def registrar_compra(cliente_id, total, descripcion=None):
    """Registra una compra para un cliente"""
    datos = {
        "cliente_id": cliente_id,
        "total": total,
        "descripcion": descripcion
    }
    
    response = requests.post(f"{API_URL}/compras", json=datos)
    
    if response.status_code == 201:
        resultado = response.json()
        print(f"✅ Compra registrada: ${resultado['compra']['total']}")
        print(f"   Puntos ganados: {resultado['compra']['puntos_ganados']}")
        print(f"   Puntos totales: {resultado['cliente']['puntos_acumulados']}")
        print(f"   Nivel actual: {resultado['cliente']['nivel_fidelidad']}")
        return resultado
    else:
        print(f"❌ Error al registrar compra")
        return None


def listar_recompensas():
    """Lista todas las recompensas disponibles"""
    response = requests.get(f"{API_URL}/recompensas")
    
    if response.status_code == 200:
        recompensas = response.json()
        print(f"\nRecompensas disponibles ({len(recompensas)}):")
        for r in recompensas:
            print(f"  - {r['nombre']}: {r['puntos_requeridos']} puntos ({r['nivel_minimo']}+)")
        return recompensas
    else:
        print(f"❌ Error al cargar recompensas")
        return []


def canjear_recompensa(cliente_id, recompensa_id):
    """Canjea una recompensa para un cliente"""
    datos = {
        "cliente_id": cliente_id,
        "recompensa_id": recompensa_id
    }
    
    response = requests.post(f"{API_URL}/canje", json=datos)
    
    if response.status_code == 201:
        resultado = response.json()
        print(f"✅ Recompensa canjeada exitosamente")
        print(f"   Código de canje: {resultado['canje']['codigo_canje']}")
        print(f"   Puntos restantes: {resultado['cliente']['puntos_acumulados']}")
        return resultado
    else:
        print(f"❌ Error: {response.json().get('error', 'Error al canjear')}")
        return None


def ver_estadisticas():
    """Muestra estadísticas generales del sistema"""
    response = requests.get(f"{API_URL}/estadisticas/general")
    
    if response.status_code == 200:
        stats = response.json()
        print("\nEstadísticas Generales:")
        print(f"  Total de clientes: {stats['total_clientes']}")
        print(f"  Total de compras: {stats['total_compras']}")
        print(f"  Total vendido: ${stats['total_vendido']:.2f}")
        print(f"  Recompensas canjeadas: {stats['total_canjes']}")
        print(f"\nDistribución por nivel:")
        for nivel, cantidad in stats['clientes_por_nivel'].items():
            print(f"  {nivel}: {cantidad} clientes")
        return stats
    else:
        print(f"❌ Error al cargar estadísticas")
        return None


def demo_completa():
    """Ejecuta una demostración completa del sistema"""
    print_section("DEMO - SISTEMA CRM SUPERMERCADO EL SABANERO")
    
    # 1. Registrar clientes de ejemplo
    print_section("1. REGISTRAR CLIENTES")
    cliente1 = registrar_cliente(
        "1234567890",
        "María",
        "González",
        "maria@example.com",
        "555-1234"
    )
    
    cliente2 = registrar_cliente(
        "0987654321",
        "Carlos",
        "Rodríguez",
        "carlos@example.com",
        "555-5678"
    )
    
    # 2. Buscar cliente
    print_section("2. BUSCAR CLIENTE")
    if cliente1:
        buscar_cliente("1234567890")
    
    # 3. Registrar compras
    print_section("3. REGISTRAR COMPRAS")
    if cliente1:
        print("\n--- Compra 1 ---")
        registrar_compra(cliente1['id'], 150.00, "Compra semanal")
        
        print("\n--- Compra 2 ---")
        registrar_compra(cliente1['id'], 200.00, "Despensa del mes")
        
        print("\n--- Compra 3 (gran compra) ---")
        registrar_compra(cliente1['id'], 500.00, "Compra especial")
    
    if cliente2:
        print("\n--- Compra de Carlos ---")
        registrar_compra(cliente2['id'], 75.50, "Compra rápida")
    
    # 4. Ver estado actualizado del cliente
    print_section("4. ESTADO ACTUALIZADO DEL CLIENTE")
    if cliente1:
        buscar_cliente("1234567890")
    
    # 5. Listar recompensas
    print_section("5. RECOMPENSAS DISPONIBLES")
    recompensas = listar_recompensas()
    
    # 6. Intentar canjear recompensa
    print_section("6. CANJEAR RECOMPENSA")
    if cliente1 and recompensas:
        # Intentar canjear la primera recompensa disponible
        print(f"\nIntentando canjear: {recompensas[0]['nombre']}")
        canjear_recompensa(cliente1['id'], recompensas[0]['id'])
    
    # 7. Ver estadísticas
    print_section("7. ESTADÍSTICAS DEL SISTEMA")
    ver_estadisticas()
    
    print_section("FIN DE LA DEMOSTRACIÓN")
    print("\n✅ Demo completada exitosamente")
    print("   Accede a http://localhost:5000 para ver el API")
    print("   Abre index.html en tu navegador para la interfaz web")


if __name__ == "__main__":
    try:
        demo_completa()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose:")
        print("   python app.py")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
