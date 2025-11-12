"""
CRM - SUPERMERCADO EL SABANERO MINIMARKET
Sistema de Identificación y Fidelización de Clientes

Este módulo define los modelos de datos para el sistema CRM.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now():
    """Helper function to get current UTC time in a timezone-aware way"""
    return datetime.now(timezone.utc)


class Cliente(db.Model):
    """Modelo para almacenar información de clientes"""
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=utc_now)
    puntos_acumulados = db.Column(db.Integer, default=0)
    nivel_fidelidad = db.Column(db.String(20), default='Bronce')  # Bronce, Plata, Oro, Platino
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    compras = db.relationship('Compra', backref='cliente', lazy=True)
    canjes = db.relationship('CanjeRecompensa', backref='cliente', lazy=True)
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'direccion': self.direccion,
            'fecha_registro': self.fecha_registro.isoformat(),
            'puntos_acumulados': self.puntos_acumulados,
            'nivel_fidelidad': self.nivel_fidelidad,
            'activo': self.activo
        }
    
    def actualizar_nivel_fidelidad(self):
        """Actualiza el nivel de fidelidad según los puntos acumulados"""
        if self.puntos_acumulados >= 10000:
            self.nivel_fidelidad = 'Platino'
        elif self.puntos_acumulados >= 5000:
            self.nivel_fidelidad = 'Oro'
        elif self.puntos_acumulados >= 2000:
            self.nivel_fidelidad = 'Plata'
        else:
            self.nivel_fidelidad = 'Bronce'


class Compra(db.Model):
    """Modelo para registrar compras de clientes"""
    __tablename__ = 'compras'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=utc_now, index=True)
    total = db.Column(db.Float, nullable=False)
    puntos_ganados = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(200), nullable=True)
    numero_factura = db.Column(db.String(50), unique=True, nullable=True)
    
    def __repr__(self):
        return f'<Compra {self.numero_factura} - ${self.total}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha': self.fecha.isoformat(),
            'total': self.total,
            'puntos_ganados': self.puntos_ganados,
            'descripcion': self.descripcion,
            'numero_factura': self.numero_factura
        }
    
    def calcular_puntos(self, multiplicador=1.0):
        """Calcula puntos basados en el total de la compra
        1 punto por cada dólar gastado, con multiplicador según nivel
        """
        puntos_base = int(self.total)
        self.puntos_ganados = int(puntos_base * multiplicador)
        return self.puntos_ganados


class Recompensa(db.Model):
    """Modelo para catálogo de recompensas disponibles"""
    __tablename__ = 'recompensas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    puntos_requeridos = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=True)  # Descuento, Producto, Servicio
    valor = db.Column(db.Float, nullable=True)  # Valor en dinero de la recompensa
    disponible = db.Column(db.Boolean, default=True)
    nivel_minimo = db.Column(db.String(20), default='Bronce')
    stock = db.Column(db.Integer, nullable=True)  # None = ilimitado
    
    # Relaciones
    canjes = db.relationship('CanjeRecompensa', backref='recompensa', lazy=True)
    
    def __repr__(self):
        return f'<Recompensa {self.nombre}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'puntos_requeridos': self.puntos_requeridos,
            'categoria': self.categoria,
            'valor': self.valor,
            'disponible': self.disponible,
            'nivel_minimo': self.nivel_minimo,
            'stock': self.stock
        }


class CanjeRecompensa(db.Model):
    """Modelo para registrar canjes de recompensas"""
    __tablename__ = 'canjes_recompensas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    recompensa_id = db.Column(db.Integer, db.ForeignKey('recompensas.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=utc_now)
    puntos_utilizados = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='Canjeado')  # Canjeado, Usado, Expirado
    codigo_canje = db.Column(db.String(20), unique=True, nullable=True)
    
    def __repr__(self):
        return f'<CanjeRecompensa {self.codigo_canje}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'recompensa_id': self.recompensa_id,
            'fecha': self.fecha.isoformat(),
            'puntos_utilizados': self.puntos_utilizados,
            'estado': self.estado,
            'codigo_canje': self.codigo_canje
        }


class Promocion(db.Model):
    """Modelo para campañas promocionales"""
    __tablename__ = 'promociones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    multiplicador_puntos = db.Column(db.Float, default=2.0)  # Puntos dobles, triples, etc.
    nivel_aplicable = db.Column(db.String(20), nullable=True)  # null = todos los niveles
    activa = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Promocion {self.nombre}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'multiplicador_puntos': self.multiplicador_puntos,
            'nivel_aplicable': self.nivel_aplicable,
            'activa': self.activa
        }
    
    def esta_activa(self):
        """Verifica si la promoción está activa en la fecha actual"""
        ahora = datetime.now(timezone.utc)
        return self.activa and self.fecha_inicio <= ahora <= self.fecha_fin
