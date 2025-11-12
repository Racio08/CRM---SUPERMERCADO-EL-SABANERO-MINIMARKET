#!/usr/bin/env python3
"""
Main CRM Application for Supermercado El Sabanero Minimarket
Command-line interface for customer relationship management
"""

import sys
from database import CRMDatabase
from datetime import datetime

class CRMApp:
    """Main CRM Application"""
    
    def __init__(self):
        """Initialize the CRM application"""
        self.db = CRMDatabase()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 2)
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
    
    def print_menu(self):
        """Print the main menu"""
        self.print_header("CRM - SUPERMERCADO EL SABANERO MINIMARKET")
        print("1.  Registrar Nuevo Cliente")
        print("2.  Buscar Cliente")
        print("3.  Ver Todos los Clientes")
        print("4.  Actualizar Información de Cliente")
        print("5.  Registrar Compra")
        print("6.  Ver Historial de Compras de Cliente")
        print("7.  Canjear Puntos de Lealtad")
        print("8.  Ver Historial de Puntos")
        print("9.  Top Clientes")
        print("10. Reporte de Ventas")
        print("0.  Salir")
        print("-" * 60)
    
    def input_with_prompt(self, prompt: str, required: bool = True) -> str:
        """Get input from user with validation"""
        while True:
            value = input(f"{prompt}: ").strip()
            if value or not required:
                return value
            print("Este campo es requerido. Por favor ingrese un valor.")
    
    def register_customer(self):
        """Register a new customer"""
        self.print_header("REGISTRAR NUEVO CLIENTE")
        
        cedula = self.input_with_prompt("Cédula")
        
        # Check if customer already exists
        existing = self.db.get_customer_by_cedula(cedula)
        if existing:
            print(f"\n❌ Ya existe un cliente con la cédula {cedula}")
            print(f"   Nombre: {existing['nombre']} {existing['apellido']}")
            return
        
        nombre = self.input_with_prompt("Nombre")
        apellido = self.input_with_prompt("Apellido")
        telefono = self.input_with_prompt("Teléfono", required=False)
        email = self.input_with_prompt("Email", required=False)
        direccion = self.input_with_prompt("Dirección", required=False)
        
        customer_id = self.db.add_customer(cedula, nombre, apellido, telefono, email, direccion)
        
        if customer_id:
            print(f"\n✓ Cliente registrado exitosamente!")
            print(f"  ID: {customer_id}")
            print(f"  Nombre: {nombre} {apellido}")
        else:
            print("\n❌ Error al registrar el cliente")
    
    def search_customer(self):
        """Search for a customer"""
        self.print_header("BUSCAR CLIENTE")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if customer:
            self.display_customer_info(customer)
        else:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
    
    def display_customer_info(self, customer: dict):
        """Display customer information"""
        print("\n" + "-" * 60)
        print(f"ID:              {customer['customer_id']}")
        print(f"Cédula:          {customer['cedula']}")
        print(f"Nombre:          {customer['nombre']} {customer['apellido']}")
        print(f"Teléfono:        {customer['telefono'] or 'N/A'}")
        print(f"Email:           {customer['email'] or 'N/A'}")
        print(f"Dirección:       {customer['direccion'] or 'N/A'}")
        print(f"Puntos:          {customer['puntos_lealtad']}")
        print(f"Registrado:      {customer['fecha_registro']}")
        print(f"Estado:          {'Activo' if customer['activo'] else 'Inactivo'}")
        print("-" * 60)
    
    def list_all_customers(self):
        """List all customers"""
        self.print_header("TODOS LOS CLIENTES")
        
        customers = self.db.list_all_customers()
        
        if not customers:
            print("No hay clientes registrados.")
            return
        
        print(f"Total de clientes: {len(customers)}\n")
        print(f"{'ID':<5} {'Cédula':<15} {'Nombre':<25} {'Teléfono':<15} {'Puntos':<10}")
        print("-" * 75)
        
        for customer in customers:
            nombre_completo = f"{customer['nombre']} {customer['apellido']}"
            print(f"{customer['customer_id']:<5} {customer['cedula']:<15} {nombre_completo:<25} "
                  f"{customer['telefono'] or 'N/A':<15} {customer['puntos_lealtad']:<10}")
    
    def update_customer(self):
        """Update customer information"""
        self.print_header("ACTUALIZAR INFORMACIÓN DE CLIENTE")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if not customer:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
            return
        
        print(f"\nCliente actual: {customer['nombre']} {customer['apellido']}")
        print("(Presione Enter para mantener el valor actual)\n")
        
        nombre = input(f"Nombre [{customer['nombre']}]: ").strip()
        apellido = input(f"Apellido [{customer['apellido']}]: ").strip()
        telefono = input(f"Teléfono [{customer['telefono'] or 'N/A'}]: ").strip()
        email = input(f"Email [{customer['email'] or 'N/A'}]: ").strip()
        direccion = input(f"Dirección [{customer['direccion'] or 'N/A'}]: ").strip()
        
        updates = {}
        if nombre:
            updates['nombre'] = nombre
        if apellido:
            updates['apellido'] = apellido
        if telefono:
            updates['telefono'] = telefono
        if email:
            updates['email'] = email
        if direccion:
            updates['direccion'] = direccion
        
        if updates:
            if self.db.update_customer(cedula, **updates):
                print("\n✓ Cliente actualizado exitosamente!")
            else:
                print("\n❌ Error al actualizar el cliente")
        else:
            print("\nNo se realizaron cambios.")
    
    def register_purchase(self):
        """Register a new purchase"""
        self.print_header("REGISTRAR COMPRA")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if not customer:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
            return
        
        print(f"\nCliente: {customer['nombre']} {customer['apellido']}")
        print(f"Puntos actuales: {customer['puntos_lealtad']}")
        
        # Get payment method
        print("\nMétodos de pago:")
        print("1. Efectivo")
        print("2. Tarjeta")
        print("3. Transferencia")
        
        metodo_choice = self.input_with_prompt("Seleccione método de pago (1-3)")
        metodos = {"1": "Efectivo", "2": "Tarjeta", "3": "Transferencia"}
        metodo_pago = metodos.get(metodo_choice, "Efectivo")
        
        # Get purchase items
        items = []
        total = 0
        
        print("\nIngrese los productos (escriba 'fin' para terminar):")
        
        while True:
            producto = input("\nProducto (o 'fin' para terminar): ").strip()
            if producto.lower() == 'fin':
                break
            
            if not producto:
                continue
            
            try:
                cantidad = int(self.input_with_prompt("Cantidad"))
                precio = float(self.input_with_prompt("Precio unitario"))
                
                subtotal = cantidad * precio
                items.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
                total += subtotal
                print(f"  Subtotal: ${subtotal:,.2f}")
            except ValueError:
                print("Error: Ingrese valores numéricos válidos")
        
        if not items:
            print("\n❌ No se agregaron productos a la compra")
            return
        
        # Confirm purchase
        print("\n" + "=" * 60)
        print("RESUMEN DE COMPRA")
        print("=" * 60)
        for item in items:
            print(f"{item['producto']:<30} x{item['cantidad']:<5} ${item['precio']:>8,.2f}  ${item['subtotal']:>10,.2f}")
        print("-" * 60)
        print(f"{'TOTAL':<47} ${total:>10,.2f}")
        puntos_a_ganar = int(total / 1000)
        print(f"\nPuntos a ganar: {puntos_a_ganar}")
        print(f"Método de pago: {metodo_pago}")
        
        confirm = input("\n¿Confirmar compra? (s/n): ").strip().lower()
        
        if confirm == 's':
            compra_id = self.db.add_purchase(customer['customer_id'], total, metodo_pago)
            
            if compra_id:
                # Add items to purchase
                for item in items:
                    self.db.add_purchase_item(compra_id, item['producto'], 
                                             item['cantidad'], item['precio'])
                
                print(f"\n✓ Compra registrada exitosamente!")
                print(f"  Número de compra: {compra_id}")
                print(f"  Total: ${total:,.2f}")
                print(f"  Puntos ganados: {puntos_a_ganar}")
                print(f"  Nuevos puntos totales: {customer['puntos_lealtad'] + puntos_a_ganar}")
            else:
                print("\n❌ Error al registrar la compra")
        else:
            print("\nCompra cancelada.")
    
    def view_purchase_history(self):
        """View customer purchase history"""
        self.print_header("HISTORIAL DE COMPRAS")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if not customer:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
            return
        
        print(f"\nCliente: {customer['nombre']} {customer['apellido']}")
        print(f"Puntos actuales: {customer['puntos_lealtad']}\n")
        
        purchases = self.db.get_customer_purchases(customer['customer_id'])
        
        if not purchases:
            print("No hay compras registradas para este cliente.")
            return
        
        print(f"{'ID':<8} {'Fecha':<20} {'Total':<15} {'Puntos':<10} {'Método Pago':<15}")
        print("-" * 70)
        
        total_gastado = 0
        for purchase in purchases:
            print(f"{purchase['compra_id']:<8} {purchase['fecha']:<20} "
                  f"${purchase['total']:>12,.2f} {purchase['puntos_ganados']:<10} "
                  f"{purchase['metodo_pago']:<15}")
            total_gastado += purchase['total']
        
        print("-" * 70)
        print(f"Total de compras: {len(purchases)}")
        print(f"Total gastado: ${total_gastado:,.2f}")
    
    def redeem_points(self):
        """Redeem loyalty points"""
        self.print_header("CANJEAR PUNTOS DE LEALTAD")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if not customer:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
            return
        
        print(f"\nCliente: {customer['nombre']} {customer['apellido']}")
        print(f"Puntos disponibles: {customer['puntos_lealtad']}")
        
        if customer['puntos_lealtad'] == 0:
            print("\nEl cliente no tiene puntos disponibles para canjear.")
            return
        
        print("\nOpciones de canje:")
        print("  - 100 puntos = $10,000 descuento")
        print("  - 50 puntos = $5,000 descuento")
        
        try:
            puntos = int(self.input_with_prompt("Puntos a canjear"))
            
            if puntos > customer['puntos_lealtad']:
                print(f"\n❌ El cliente solo tiene {customer['puntos_lealtad']} puntos disponibles")
                return
            
            if puntos <= 0:
                print("\n❌ Debe canjear al menos 1 punto")
                return
            
            descuento = puntos * 100  # 100 pesos por punto
            descripcion = self.input_with_prompt("Descripción del canje", required=False) or "Canje de puntos"
            
            confirm = input(f"\n¿Confirmar canje de {puntos} puntos (${descuento:,} de descuento)? (s/n): ").strip().lower()
            
            if confirm == 's':
                if self.db.redeem_points(customer['customer_id'], puntos, descripcion):
                    print(f"\n✓ Puntos canjeados exitosamente!")
                    print(f"  Puntos canjeados: {puntos}")
                    print(f"  Descuento aplicado: ${descuento:,}")
                    print(f"  Puntos restantes: {customer['puntos_lealtad'] - puntos}")
                else:
                    print("\n❌ Error al canjear puntos")
            else:
                print("\nCanje cancelado.")
        except ValueError:
            print("\n❌ Debe ingresar un número válido de puntos")
    
    def view_points_history(self):
        """View loyalty points history"""
        self.print_header("HISTORIAL DE PUNTOS")
        
        cedula = self.input_with_prompt("Cédula del cliente")
        customer = self.db.get_customer_by_cedula(cedula)
        
        if not customer:
            print(f"\n❌ No se encontró cliente con la cédula {cedula}")
            return
        
        print(f"\nCliente: {customer['nombre']} {customer['apellido']}")
        print(f"Puntos actuales: {customer['puntos_lealtad']}\n")
        
        history = self.db.get_points_history(customer['customer_id'])
        
        if not history:
            print("No hay historial de puntos para este cliente.")
            return
        
        print(f"{'Fecha':<20} {'Tipo':<12} {'Puntos':<10} {'Descripción':<30}")
        print("-" * 75)
        
        for transaction in history:
            puntos_str = f"+{transaction['puntos']}" if transaction['puntos'] > 0 else str(transaction['puntos'])
            print(f"{transaction['fecha']:<20} {transaction['tipo']:<12} "
                  f"{puntos_str:<10} {transaction['descripcion']:<30}")
    
    def show_top_customers(self):
        """Show top customers by purchases"""
        self.print_header("TOP CLIENTES")
        
        try:
            limit = int(input("¿Cuántos clientes mostrar? [10]: ").strip() or "10")
        except ValueError:
            limit = 10
        
        top_customers = self.db.get_top_customers(limit)
        
        if not top_customers:
            print("No hay clientes registrados.")
            return
        
        print(f"\nTop {len(top_customers)} clientes por total gastado:\n")
        print(f"{'#':<4} {'Nombre':<25} {'Compras':<10} {'Total Gastado':<15} {'Puntos':<10}")
        print("-" * 70)
        
        for idx, customer in enumerate(top_customers, 1):
            nombre_completo = f"{customer['nombre']} {customer['apellido']}"
            print(f"{idx:<4} {nombre_completo:<25} {customer['total_compras']:<10} "
                  f"${customer['total_gastado']:>12,.2f} {customer['puntos_lealtad']:<10}")
    
    def show_sales_report(self):
        """Show sales report"""
        self.print_header("REPORTE DE VENTAS")
        
        try:
            days = int(input("¿Últimos cuántos días? [30]: ").strip() or "30")
        except ValueError:
            days = 30
        
        summary = self.db.get_sales_summary(days)
        
        print(f"\nReporte de los últimos {days} días:\n")
        print(f"Total de compras:      {summary['total_compras']}")
        print(f"Total de ventas:       ${summary['total_ventas']:,.2f}")
        print(f"Promedio por compra:   ${summary['promedio_compra']:,.2f}")
        print(f"Clientes únicos:       {summary['clientes_unicos']}")
    
    def run(self):
        """Main application loop"""
        print("\n¡Bienvenido al Sistema CRM!")
        print("Supermercado El Sabanero Minimarket")
        
        while self.running:
            self.print_menu()
            choice = input("Seleccione una opción: ").strip()
            
            if choice == '1':
                self.register_customer()
            elif choice == '2':
                self.search_customer()
            elif choice == '3':
                self.list_all_customers()
            elif choice == '4':
                self.update_customer()
            elif choice == '5':
                self.register_purchase()
            elif choice == '6':
                self.view_purchase_history()
            elif choice == '7':
                self.redeem_points()
            elif choice == '8':
                self.view_points_history()
            elif choice == '9':
                self.show_top_customers()
            elif choice == '10':
                self.show_sales_report()
            elif choice == '0':
                self.running = False
                print("\n¡Gracias por usar el Sistema CRM!")
                print("¡Hasta luego!")
            else:
                print("\n❌ Opción inválida. Por favor seleccione una opción del menú.")
            
            if self.running and choice != '0':
                input("\nPresione Enter para continuar...")
        
        # Close database connection
        self.db.close()

def main():
    """Main entry point"""
    try:
        app = CRMApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        print("¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
