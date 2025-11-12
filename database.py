#!/usr/bin/env python3
"""
Database module for CRM - Supermercado El Sabanero Minimarket
Handles all database operations including customer management, purchases, and loyalty points
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class CRMDatabase:
    """Database handler for the CRM system"""
    
    def __init__(self, db_name: str = "crm_sabanero.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary tables for the CRM system"""
        
        # Customers table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula VARCHAR(20) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                email VARCHAR(100),
                direccion TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                puntos_lealtad INTEGER DEFAULT 0,
                activo BOOLEAN DEFAULT 1
            )
        """)
        
        # Purchases table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                compra_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total DECIMAL(10, 2) NOT NULL,
                puntos_ganados INTEGER DEFAULT 0,
                metodo_pago VARCHAR(50),
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        # Purchase items table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items_compra (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                producto VARCHAR(200) NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10, 2) NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras (compra_id)
            )
        """)
        
        # Loyalty transactions table (points earned/redeemed)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacciones_puntos (
                transaccion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                puntos INTEGER NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                descripcion TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        self.conn.commit()
    
    # Customer Management Methods
    
    def add_customer(self, cedula: str, nombre: str, apellido: str, 
                    telefono: str = "", email: str = "", direccion: str = "") -> Optional[int]:
        """Add a new customer to the database"""
        try:
            self.cursor.execute("""
                INSERT INTO customers (cedula, nombre, apellido, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cedula, nombre, apellido, telefono, email, direccion))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_customer_by_cedula(self, cedula: str) -> Optional[Dict]:
        """Get customer information by cedula"""
        self.cursor.execute("""
            SELECT customer_id, cedula, nombre, apellido, telefono, email, 
                   direccion, fecha_registro, puntos_lealtad, activo
            FROM customers
            WHERE cedula = ?
        """, (cedula,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                'customer_id': row[0],
                'cedula': row[1],
                'nombre': row[2],
                'apellido': row[3],
                'telefono': row[4],
                'email': row[5],
                'direccion': row[6],
                'fecha_registro': row[7],
                'puntos_lealtad': row[8],
                'activo': row[9]
            }
        return None
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        """Get customer information by ID"""
        self.cursor.execute("""
            SELECT customer_id, cedula, nombre, apellido, telefono, email, 
                   direccion, fecha_registro, puntos_lealtad, activo
            FROM customers
            WHERE customer_id = ?
        """, (customer_id,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                'customer_id': row[0],
                'cedula': row[1],
                'nombre': row[2],
                'apellido': row[3],
                'telefono': row[4],
                'email': row[5],
                'direccion': row[6],
                'fecha_registro': row[7],
                'puntos_lealtad': row[8],
                'activo': row[9]
            }
        return None
    
    def update_customer(self, cedula: str, **kwargs) -> bool:
        """Update customer information"""
        customer = self.get_customer_by_cedula(cedula)
        if not customer:
            return False
        
        allowed_fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion']
        updates = []
        values = []
        
        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = ?")
                values.append(kwargs[field])
        
        if not updates:
            return False
        
        values.append(cedula)
        query = f"UPDATE customers SET {', '.join(updates)} WHERE cedula = ?"
        
        self.cursor.execute(query, values)
        self.conn.commit()
        return True
    
    def list_all_customers(self, active_only: bool = True) -> List[Dict]:
        """List all customers"""
        query = """
            SELECT customer_id, cedula, nombre, apellido, telefono, email, 
                   direccion, fecha_registro, puntos_lealtad, activo
            FROM customers
        """
        if active_only:
            query += " WHERE activo = 1"
        query += " ORDER BY apellido, nombre"
        
        self.cursor.execute(query)
        customers = []
        for row in self.cursor.fetchall():
            customers.append({
                'customer_id': row[0],
                'cedula': row[1],
                'nombre': row[2],
                'apellido': row[3],
                'telefono': row[4],
                'email': row[5],
                'direccion': row[6],
                'fecha_registro': row[7],
                'puntos_lealtad': row[8],
                'activo': row[9]
            })
        return customers
    
    def deactivate_customer(self, cedula: str) -> bool:
        """Deactivate a customer"""
        self.cursor.execute("""
            UPDATE customers SET activo = 0 WHERE cedula = ?
        """, (cedula,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # Purchase Management Methods
    
    def add_purchase(self, customer_id: int, total: float, 
                    metodo_pago: str = "Efectivo") -> Optional[int]:
        """Add a new purchase"""
        # Calculate loyalty points: 1 point per 1000 pesos
        puntos_ganados = int(total / 1000)
        
        try:
            self.cursor.execute("""
                INSERT INTO compras (customer_id, total, puntos_ganados, metodo_pago)
                VALUES (?, ?, ?, ?)
            """, (customer_id, total, puntos_ganados, metodo_pago))
            
            compra_id = self.cursor.lastrowid
            
            # Update customer loyalty points
            self.cursor.execute("""
                UPDATE customers SET puntos_lealtad = puntos_lealtad + ?
                WHERE customer_id = ?
            """, (puntos_ganados, customer_id))
            
            # Record points transaction
            self.cursor.execute("""
                INSERT INTO transacciones_puntos (customer_id, puntos, tipo, descripcion)
                VALUES (?, ?, 'GANADO', ?)
            """, (customer_id, puntos_ganados, f"Compra #{compra_id}"))
            
            self.conn.commit()
            return compra_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding purchase: {e}")
            return None
    
    def add_purchase_item(self, compra_id: int, producto: str, 
                         cantidad: int, precio_unitario: float) -> bool:
        """Add an item to a purchase"""
        subtotal = cantidad * precio_unitario
        try:
            self.cursor.execute("""
                INSERT INTO items_compra (compra_id, producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (compra_id, producto, cantidad, precio_unitario, subtotal))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding purchase item: {e}")
            return False
    
    def get_customer_purchases(self, customer_id: int) -> List[Dict]:
        """Get all purchases for a customer"""
        self.cursor.execute("""
            SELECT compra_id, fecha, total, puntos_ganados, metodo_pago
            FROM compras
            WHERE customer_id = ?
            ORDER BY fecha DESC
        """, (customer_id,))
        
        purchases = []
        for row in self.cursor.fetchall():
            purchases.append({
                'compra_id': row[0],
                'fecha': row[1],
                'total': row[2],
                'puntos_ganados': row[3],
                'metodo_pago': row[4]
            })
        return purchases
    
    def get_purchase_details(self, compra_id: int) -> Dict:
        """Get detailed information about a purchase"""
        self.cursor.execute("""
            SELECT c.compra_id, c.customer_id, c.fecha, c.total, c.puntos_ganados, c.metodo_pago,
                   cu.cedula, cu.nombre, cu.apellido
            FROM compras c
            JOIN customers cu ON c.customer_id = cu.customer_id
            WHERE c.compra_id = ?
        """, (compra_id,))
        
        row = self.cursor.fetchone()
        if not row:
            return None
        
        # Get purchase items
        self.cursor.execute("""
            SELECT producto, cantidad, precio_unitario, subtotal
            FROM items_compra
            WHERE compra_id = ?
        """, (compra_id,))
        
        items = []
        for item_row in self.cursor.fetchall():
            items.append({
                'producto': item_row[0],
                'cantidad': item_row[1],
                'precio_unitario': item_row[2],
                'subtotal': item_row[3]
            })
        
        return {
            'compra_id': row[0],
            'customer_id': row[1],
            'fecha': row[2],
            'total': row[3],
            'puntos_ganados': row[4],
            'metodo_pago': row[5],
            'cedula': row[6],
            'nombre_cliente': f"{row[7]} {row[8]}",
            'items': items
        }
    
    # Loyalty Points Methods
    
    def redeem_points(self, customer_id: int, puntos: int, descripcion: str = "") -> bool:
        """Redeem loyalty points"""
        customer = self.get_customer_by_id(customer_id)
        if not customer or customer['puntos_lealtad'] < puntos:
            return False
        
        try:
            self.cursor.execute("""
                UPDATE customers SET puntos_lealtad = puntos_lealtad - ?
                WHERE customer_id = ?
            """, (puntos, customer_id))
            
            self.cursor.execute("""
                INSERT INTO transacciones_puntos (customer_id, puntos, tipo, descripcion)
                VALUES (?, ?, 'CANJEADO', ?)
            """, (customer_id, -puntos, descripcion or "Canje de puntos"))
            
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error redeeming points: {e}")
            return False
    
    def get_points_history(self, customer_id: int) -> List[Dict]:
        """Get loyalty points transaction history"""
        self.cursor.execute("""
            SELECT transaccion_id, puntos, tipo, descripcion, fecha
            FROM transacciones_puntos
            WHERE customer_id = ?
            ORDER BY fecha DESC
        """, (customer_id,))
        
        history = []
        for row in self.cursor.fetchall():
            history.append({
                'transaccion_id': row[0],
                'puntos': row[1],
                'tipo': row[2],
                'descripcion': row[3],
                'fecha': row[4]
            })
        return history
    
    # Reports Methods
    
    def get_top_customers(self, limit: int = 10) -> List[Dict]:
        """Get top customers by purchase amount"""
        self.cursor.execute("""
            SELECT c.customer_id, c.cedula, c.nombre, c.apellido, 
                   COUNT(co.compra_id) as total_compras,
                   SUM(co.total) as total_gastado,
                   c.puntos_lealtad
            FROM customers c
            LEFT JOIN compras co ON c.customer_id = co.customer_id
            WHERE c.activo = 1
            GROUP BY c.customer_id
            ORDER BY total_gastado DESC
            LIMIT ?
        """, (limit,))
        
        top_customers = []
        for row in self.cursor.fetchall():
            top_customers.append({
                'customer_id': row[0],
                'cedula': row[1],
                'nombre': row[2],
                'apellido': row[3],
                'total_compras': row[4] or 0,
                'total_gastado': row[5] or 0,
                'puntos_lealtad': row[6]
            })
        return top_customers
    
    def get_sales_summary(self, days: int = 30) -> Dict:
        """Get sales summary for the last N days"""
        self.cursor.execute("""
            SELECT COUNT(*) as total_compras,
                   SUM(total) as total_ventas,
                   AVG(total) as promedio_compra,
                   COUNT(DISTINCT customer_id) as clientes_unicos
            FROM compras
            WHERE fecha >= datetime('now', '-' || ? || ' days')
        """, (days,))
        
        row = self.cursor.fetchone()
        return {
            'total_compras': row[0] or 0,
            'total_ventas': row[1] or 0,
            'promedio_compra': row[2] or 0,
            'clientes_unicos': row[3] or 0
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
