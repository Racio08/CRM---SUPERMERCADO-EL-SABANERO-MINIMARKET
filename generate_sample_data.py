#!/usr/bin/env python3
"""
Sample data generator for CRM - Supermercado El Sabanero Minimarket
Creates sample customers and purchases for testing purposes
"""

from database import CRMDatabase
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample data for testing"""
    db = CRMDatabase()
    
    print("Generando datos de ejemplo para el CRM...")
    print("-" * 60)
    
    # Sample customers
    customers = [
        ("12345678", "Juan", "Pérez", "555-0101", "juan.perez@email.com", "Calle Principal #123"),
        ("23456789", "María", "González", "555-0102", "maria.gonzalez@email.com", "Avenida Central #456"),
        ("34567890", "Carlos", "Rodríguez", "555-0103", "carlos.rodriguez@email.com", "Barrio Norte #789"),
        ("45678901", "Ana", "Martínez", "555-0104", "ana.martinez@email.com", "Zona Sur #321"),
        ("56789012", "Luis", "López", "555-0105", "luis.lopez@email.com", "Sector Este #654"),
        ("67890123", "Carmen", "Sánchez", "555-0106", "carmen.sanchez@email.com", "Urbanización Oeste #987"),
        ("78901234", "José", "Ramírez", "555-0107", "jose.ramirez@email.com", "Residencias Centro #147"),
        ("89012345", "Laura", "Torres", "555-0108", "laura.torres@email.com", "Conjunto Habitacional #258"),
        ("90123456", "Pedro", "Flores", "555-0109", "pedro.flores@email.com", "Barrio El Sabanero #369"),
        ("01234567", "Sofia", "Vargas", "555-0110", "sofia.vargas@email.com", "Calle Segunda #741"),
    ]
    
    customer_ids = []
    
    print("\n1. Registrando clientes...")
    for cedula, nombre, apellido, telefono, email, direccion in customers:
        customer_id = db.add_customer(cedula, nombre, apellido, telefono, email, direccion)
        if customer_id:
            customer_ids.append(customer_id)
            print(f"   ✓ {nombre} {apellido} (ID: {customer_id})")
        else:
            # Customer might already exist
            customer = db.get_customer_by_cedula(cedula)
            if customer:
                customer_ids.append(customer['customer_id'])
                print(f"   - {nombre} {apellido} (Ya existe)")
    
    # Sample products
    productos = [
        ("Arroz 1kg", 2500, 3500),
        ("Aceite de cocina 1L", 8000, 12000),
        ("Azúcar 1kg", 2000, 3000),
        ("Leche 1L", 3000, 4000),
        ("Pan", 1500, 2500),
        ("Huevos x12", 6000, 8000),
        ("Pasta 500g", 2500, 3500),
        ("Sal 1kg", 1000, 1500),
        ("Café 250g", 8000, 12000),
        ("Jabón de baño", 2000, 4000),
        ("Papel higiénico x4", 5000, 7000),
        ("Detergente 1kg", 6000, 9000),
        ("Atún enlatado", 3000, 4500),
        ("Sardinas enlatadas", 2500, 3500),
        ("Frijoles 500g", 3000, 4000),
        ("Tomate", 1000, 2000),
        ("Cebolla", 800, 1500),
        ("Papa 1kg", 2000, 3000),
        ("Zanahoria", 1500, 2500),
        ("Plátano", 1000, 2000),
    ]
    
    metodos_pago = ["Efectivo", "Tarjeta", "Transferencia"]
    
    print("\n2. Generando compras de ejemplo...")
    total_compras = 0
    
    # Generate purchases for the last 30 days
    for i in range(50):  # 50 sample purchases
        customer_id = random.choice(customer_ids)
        
        # Random date in the last 30 days
        days_ago = random.randint(0, 30)
        
        # Select random number of products (1-5)
        num_products = random.randint(1, 5)
        selected_products = random.sample(productos, num_products)
        
        # Create purchase
        metodo_pago = random.choice(metodos_pago)
        
        total = 0
        items = []
        for producto, precio_min, precio_max in selected_products:
            cantidad = random.randint(1, 3)
            precio = random.randint(precio_min, precio_max)
            subtotal = cantidad * precio
            total += subtotal
            items.append((producto, cantidad, precio))
        
        compra_id = db.add_purchase(customer_id, total, metodo_pago)
        
        if compra_id:
            for producto, cantidad, precio in items:
                db.add_purchase_item(compra_id, producto, cantidad, precio)
            
            total_compras += 1
            if i % 10 == 0:
                print(f"   ✓ Compra #{compra_id} - Total: ${total:,.2f}")
    
    print(f"\n   Total de compras generadas: {total_compras}")
    
    print("\n3. Generando algunos canjes de puntos...")
    # Redeem some points for random customers
    for i in range(5):
        customer_id = random.choice(customer_ids)
        customer = db.get_customer_by_id(customer_id)
        
        if customer and customer['puntos_lealtad'] >= 50:
            puntos_canjear = min(50, customer['puntos_lealtad'])
            if db.redeem_points(customer_id, puntos_canjear, "Descuento en compra"):
                print(f"   ✓ {customer['nombre']} {customer['apellido']} canjeó {puntos_canjear} puntos")
    
    print("\n" + "=" * 60)
    print("¡Datos de ejemplo generados exitosamente!")
    print("=" * 60)
    
    # Show summary
    summary = db.get_sales_summary(30)
    print(f"\nResumen:")
    print(f"  Clientes registrados: {len(customer_ids)}")
    print(f"  Total de compras:     {summary['total_compras']}")
    print(f"  Total de ventas:      ${summary['total_ventas']:,.2f}")
    print(f"  Promedio por compra:  ${summary['promedio_compra']:,.2f}")
    
    db.close()

if __name__ == "__main__":
    generate_sample_data()
