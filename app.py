"""
CRM - SUPERMERCADO EL SABANERO MINIMARKET
API REST para el sistema de fidelización

Este módulo contiene las rutas y lógica de la API.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import random
import string
from models import db, Cliente, Compra, Recompensa, CanjeRecompensa, Promocion


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_sabanero.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Habilitar CORS para todas las rutas
    CORS(app)
    
    # Inicializar base de datos
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        inicializar_datos_demo()
    
    # ==================== RUTAS DE CLIENTES ====================
    
    @app.route('/api/clientes', methods=['GET'])
    def listar_clientes():
        """Lista todos los clientes activos"""
        clientes = Cliente.query.filter_by(activo=True).all()
        return jsonify([cliente.to_dict() for cliente in clientes])
    
    @app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
    def obtener_cliente(cliente_id):
        """Obtiene información detallada de un cliente"""
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify(cliente.to_dict())
    
    @app.route('/api/clientes/buscar/<cedula>', methods=['GET'])
    def buscar_cliente_por_cedula(cedula):
        """Busca un cliente por su cédula"""
        cliente = Cliente.query.filter_by(cedula=cedula, activo=True).first()
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        return jsonify(cliente.to_dict())
    
    @app.route('/api/clientes', methods=['POST'])
    def registrar_cliente():
        """Registra un nuevo cliente en el sistema"""
        datos = request.get_json()
        
        # Validar datos requeridos
        if not datos.get('cedula') or not datos.get('nombre') or not datos.get('apellido'):
            return jsonify({'error': 'Cédula, nombre y apellido son obligatorios'}), 400
        
        # Verificar si ya existe
        if Cliente.query.filter_by(cedula=datos['cedula']).first():
            return jsonify({'error': 'Ya existe un cliente con esta cédula'}), 400
        
        # Crear nuevo cliente
        nuevo_cliente = Cliente(
            cedula=datos['cedula'],
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            email=datos.get('email'),
            telefono=datos.get('telefono'),
            direccion=datos.get('direccion'),
            fecha_nacimiento=datetime.fromisoformat(datos['fecha_nacimiento']) if datos.get('fecha_nacimiento') else None
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        return jsonify(nuevo_cliente.to_dict()), 201
    
    @app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
    def actualizar_cliente(cliente_id):
        """Actualiza información de un cliente"""
        cliente = Cliente.query.get_or_404(cliente_id)
        datos = request.get_json()
        
        # Actualizar campos permitidos
        if 'nombre' in datos:
            cliente.nombre = datos['nombre']
        if 'apellido' in datos:
            cliente.apellido = datos['apellido']
        if 'email' in datos:
            cliente.email = datos['email']
        if 'telefono' in datos:
            cliente.telefono = datos['telefono']
        if 'direccion' in datos:
            cliente.direccion = datos['direccion']
        
        db.session.commit()
        return jsonify(cliente.to_dict())
    
    # ==================== RUTAS DE COMPRAS ====================
    
    @app.route('/api/compras', methods=['POST'])
    def registrar_compra():
        """Registra una compra y asigna puntos al cliente"""
        datos = request.get_json()
        
        # Validar datos
        if not datos.get('cliente_id') or not datos.get('total'):
            return jsonify({'error': 'cliente_id y total son obligatorios'}), 400
        
        cliente = Cliente.query.get_or_404(datos['cliente_id'])
        
        # Crear compra
        compra = Compra(
            cliente_id=cliente.id,
            total=float(datos['total']),
            descripcion=datos.get('descripcion', ''),
            numero_factura=datos.get('numero_factura', f'FAC-{random.randint(10000, 99999)}')
        )
        
        # Calcular multiplicador según nivel y promociones
        multiplicador = obtener_multiplicador_puntos(cliente)
        compra.calcular_puntos(multiplicador)
        
        # Agregar puntos al cliente
        cliente.puntos_acumulados += compra.puntos_ganados
        cliente.actualizar_nivel_fidelidad()
        
        db.session.add(compra)
        db.session.commit()
        
        return jsonify({
            'compra': compra.to_dict(),
            'cliente': cliente.to_dict(),
            'mensaje': f'¡Compra registrada! Ganaste {compra.puntos_ganados} puntos'
        }), 201
    
    @app.route('/api/clientes/<int:cliente_id>/compras', methods=['GET'])
    def historial_compras(cliente_id):
        """Obtiene el historial de compras de un cliente"""
        cliente = Cliente.query.get_or_404(cliente_id)
        compras = Compra.query.filter_by(cliente_id=cliente_id).order_by(Compra.fecha.desc()).all()
        
        return jsonify({
            'cliente': cliente.to_dict(),
            'compras': [compra.to_dict() for compra in compras],
            'total_compras': len(compras),
            'total_gastado': sum(c.total for c in compras)
        })
    
    # ==================== RUTAS DE RECOMPENSAS ====================
    
    @app.route('/api/recompensas', methods=['GET'])
    def listar_recompensas():
        """Lista todas las recompensas disponibles"""
        recompensas = Recompensa.query.filter_by(disponible=True).all()
        return jsonify([r.to_dict() for r in recompensas])
    
    @app.route('/api/recompensas', methods=['POST'])
    def crear_recompensa():
        """Crea una nueva recompensa en el catálogo"""
        datos = request.get_json()
        
        recompensa = Recompensa(
            nombre=datos['nombre'],
            descripcion=datos.get('descripcion'),
            puntos_requeridos=int(datos['puntos_requeridos']),
            categoria=datos.get('categoria', 'Descuento'),
            valor=float(datos.get('valor', 0)),
            nivel_minimo=datos.get('nivel_minimo', 'Bronce'),
            stock=datos.get('stock')
        )
        
        db.session.add(recompensa)
        db.session.commit()
        
        return jsonify(recompensa.to_dict()), 201
    
    @app.route('/api/clientes/<int:cliente_id>/recompensas-disponibles', methods=['GET'])
    def recompensas_disponibles_cliente(cliente_id):
        """Lista recompensas que el cliente puede canjear"""
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Niveles de jerarquía
        jerarquia = {'Bronce': 0, 'Plata': 1, 'Oro': 2, 'Platino': 3}
        nivel_cliente = jerarquia.get(cliente.nivel_fidelidad, 0)
        
        recompensas = Recompensa.query.filter(
            Recompensa.disponible == True,
            Recompensa.puntos_requeridos <= cliente.puntos_acumulados
        ).all()
        
        # Filtrar por nivel
        recompensas_validas = [
            r for r in recompensas 
            if jerarquia.get(r.nivel_minimo, 0) <= nivel_cliente
        ]
        
        return jsonify([r.to_dict() for r in recompensas_validas])
    
    @app.route('/api/canje', methods=['POST'])
    def canjear_recompensa():
        """Permite a un cliente canjear puntos por una recompensa"""
        datos = request.get_json()
        
        cliente = Cliente.query.get_or_404(datos['cliente_id'])
        recompensa = Recompensa.query.get_or_404(datos['recompensa_id'])
        
        # Validaciones
        if cliente.puntos_acumulados < recompensa.puntos_requeridos:
            return jsonify({'error': 'Puntos insuficientes'}), 400
        
        if recompensa.stock is not None and recompensa.stock <= 0:
            return jsonify({'error': 'Recompensa agotada'}), 400
        
        # Generar código de canje único
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Crear canje
        canje = CanjeRecompensa(
            cliente_id=cliente.id,
            recompensa_id=recompensa.id,
            puntos_utilizados=recompensa.puntos_requeridos,
            codigo_canje=codigo
        )
        
        # Descontar puntos
        cliente.puntos_acumulados -= recompensa.puntos_requeridos
        cliente.actualizar_nivel_fidelidad()
        
        # Actualizar stock
        if recompensa.stock is not None:
            recompensa.stock -= 1
        
        db.session.add(canje)
        db.session.commit()
        
        return jsonify({
            'canje': canje.to_dict(),
            'cliente': cliente.to_dict(),
            'recompensa': recompensa.to_dict(),
            'mensaje': f'¡Recompensa canjeada! Código: {codigo}'
        }), 201
    
    @app.route('/api/clientes/<int:cliente_id>/canjes', methods=['GET'])
    def historial_canjes(cliente_id):
        """Obtiene el historial de canjes de un cliente"""
        cliente = Cliente.query.get_or_404(cliente_id)
        canjes = CanjeRecompensa.query.filter_by(cliente_id=cliente_id).order_by(CanjeRecompensa.fecha.desc()).all()
        
        resultado = []
        for canje in canjes:
            canje_dict = canje.to_dict()
            canje_dict['recompensa'] = canje.recompensa.to_dict()
            resultado.append(canje_dict)
        
        return jsonify(resultado)
    
    # ==================== RUTAS DE PROMOCIONES ====================
    
    @app.route('/api/promociones', methods=['GET'])
    def listar_promociones():
        """Lista todas las promociones activas"""
        ahora = datetime.now(timezone.utc)
        promociones = Promocion.query.filter(
            Promocion.activa == True,
            Promocion.fecha_inicio <= ahora,
            Promocion.fecha_fin >= ahora
        ).all()
        return jsonify([p.to_dict() for p in promociones])
    
    @app.route('/api/promociones', methods=['POST'])
    def crear_promocion():
        """Crea una nueva promoción"""
        datos = request.get_json()
        
        promocion = Promocion(
            nombre=datos['nombre'],
            descripcion=datos.get('descripcion'),
            fecha_inicio=datetime.fromisoformat(datos['fecha_inicio']),
            fecha_fin=datetime.fromisoformat(datos['fecha_fin']),
            multiplicador_puntos=float(datos.get('multiplicador_puntos', 2.0)),
            nivel_aplicable=datos.get('nivel_aplicable')
        )
        
        db.session.add(promocion)
        db.session.commit()
        
        return jsonify(promocion.to_dict()), 201
    
    # ==================== RUTAS DE ESTADÍSTICAS ====================
    
    @app.route('/api/estadisticas/general', methods=['GET'])
    def estadisticas_generales():
        """Obtiene estadísticas generales del sistema"""
        total_clientes = Cliente.query.filter_by(activo=True).count()
        total_compras = Compra.query.count()
        total_vendido = db.session.query(db.func.sum(Compra.total)).scalar() or 0
        total_canjes = CanjeRecompensa.query.count()
        
        # Distribución por nivel
        clientes_por_nivel = {}
        for nivel in ['Bronce', 'Plata', 'Oro', 'Platino']:
            clientes_por_nivel[nivel] = Cliente.query.filter_by(
                nivel_fidelidad=nivel, 
                activo=True
            ).count()
        
        return jsonify({
            'total_clientes': total_clientes,
            'total_compras': total_compras,
            'total_vendido': round(total_vendido, 2),
            'total_canjes': total_canjes,
            'clientes_por_nivel': clientes_por_nivel
        })
    
    @app.route('/api/estadisticas/clientes/top', methods=['GET'])
    def top_clientes():
        """Obtiene los clientes más activos"""
        limite = request.args.get('limite', 10, type=int)
        
        clientes = Cliente.query.filter_by(activo=True).order_by(
            Cliente.puntos_acumulados.desc()
        ).limit(limite).all()
        
        return jsonify([cliente.to_dict() for cliente in clientes])
    
    # ==================== RUTA PRINCIPAL ====================
    
    @app.route('/')
    def index():
        """Página de inicio con información del API"""
        return jsonify({
            'nombre': 'CRM - SUPERMERCADO EL SABANERO MINIMARKET',
            'version': '1.0.0',
            'descripcion': 'Sistema de Identificación y Fidelización de Clientes',
            'endpoints': {
                'clientes': '/api/clientes',
                'compras': '/api/compras',
                'recompensas': '/api/recompensas',
                'promociones': '/api/promociones',
                'estadisticas': '/api/estadisticas/general'
            }
        })
    
    return app


def obtener_multiplicador_puntos(cliente):
    """Calcula el multiplicador de puntos según promociones y nivel"""
    multiplicador = 1.0
    
    # Multiplicador base por nivel
    multiplicadores_nivel = {
        'Bronce': 1.0,
        'Plata': 1.2,
        'Oro': 1.5,
        'Platino': 2.0
    }
    multiplicador *= multiplicadores_nivel.get(cliente.nivel_fidelidad, 1.0)
    
    # Verificar promociones activas
    ahora = datetime.now(timezone.utc)
    promociones = Promocion.query.filter(
        Promocion.activa == True,
        Promocion.fecha_inicio <= ahora,
        Promocion.fecha_fin >= ahora
    ).all()
    
    for promo in promociones:
        if promo.nivel_aplicable is None or promo.nivel_aplicable == cliente.nivel_fidelidad:
            multiplicador *= promo.multiplicador_puntos
            break  # Solo aplicar una promoción
    
    return multiplicador


def inicializar_datos_demo():
    """Inicializa la base de datos con datos de demostración"""
    # Solo inicializar si no hay datos
    if Cliente.query.count() > 0:
        return
    
    # Crear recompensas de ejemplo
    recompensas_demo = [
        Recompensa(
            nombre='Descuento $5',
            descripcion='$5 de descuento en tu próxima compra',
            puntos_requeridos=500,
            categoria='Descuento',
            valor=5.0,
            nivel_minimo='Bronce'
        ),
        Recompensa(
            nombre='Descuento $10',
            descripcion='$10 de descuento en tu próxima compra',
            puntos_requeridos=1000,
            categoria='Descuento',
            valor=10.0,
            nivel_minimo='Plata'
        ),
        Recompensa(
            nombre='Producto Gratis',
            descripcion='Un producto de la línea premium gratis',
            puntos_requeridos=2000,
            categoria='Producto',
            valor=15.0,
            nivel_minimo='Oro'
        ),
        Recompensa(
            nombre='Canasta Premium',
            descripcion='Canasta de productos premium valorada en $50',
            puntos_requeridos=5000,
            categoria='Producto',
            valor=50.0,
            nivel_minimo='Platino'
        )
    ]
    
    for recompensa in recompensas_demo:
        db.session.add(recompensa)
    
    # Crear una promoción de ejemplo
    promocion = Promocion(
        nombre='Puntos Dobles Fin de Semana',
        descripcion='Gana el doble de puntos en tus compras de fin de semana',
        fecha_inicio=datetime.now(timezone.utc),
        fecha_fin=datetime.now(timezone.utc) + timedelta(days=30),
        multiplicador_puntos=2.0,
        activa=True
    )
    db.session.add(promocion)
    
    db.session.commit()
    print("✓ Datos de demostración inicializados")


if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("CRM - SUPERMERCADO EL SABANERO MINIMARKET")
    print("Sistema de Identificación y Fidelización de Clientes")
    print("=" * 60)
    print("\nServidor iniciado en: http://localhost:5000")
    print("API Endpoints disponibles:")
    print("  - GET  /api/clientes")
    print("  - POST /api/clientes")
    print("  - POST /api/compras")
    print("  - GET  /api/recompensas")
    print("  - POST /api/canje")
    print("  - GET  /api/estadisticas/general")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
