from django.db import models
from django.contrib.auth.models import User

# MODELOS
class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('PA', 'Pasaporte'),
        ('NIT', 'NIT'),
    ]
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decir'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Información de Identificación
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default='CC')
    numero_documento = models.CharField(max_length=20, unique=True)
    
    # Información Personal
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    
    # Información de Contacto
    telefono = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, blank=True)
    email_alternativo = models.EmailField(blank=True)
    
    # Dirección
    direccion = models.CharField(max_length=255, default='Sin especificar')
    barrio = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, default='Bogotá')
    departamento = models.CharField(max_length=100, default='Cundinamarca')
    codigo_postal = models.CharField(max_length=10, blank=True)
    
    # Información del CRM
    nivel = models.CharField(max_length=10, default='Bronce')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    # Preferencias
    acepta_promociones = models.BooleanField(default=True)
    acepta_notificaciones = models.BooleanField(default=True)
    
    # Notas internas
    notas = models.TextField(blank=True, help_text="Notas internas sobre el cliente")

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.numero_documento}"
    
    def edad(self):
        """Calcula la edad del cliente"""
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50)
    fecha_compra = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    sucursal = models.CharField(max_length=100)
    registrada = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.user.username}"

class Punto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    puntos_obtenidos = models.IntegerField()
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, default='Compra')

    def __str__(self):
        return f"{self.cliente.user.username} - {self.puntos_obtenidos} puntos"

class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    multiplicador_puntos = models.FloatField(default=1.0)

    def __str__(self):
        return self.nombre

class Premio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    puntos_requeridos = models.IntegerField()
    fecha_otorgado = models.DateField(auto_now_add=True)
    entregado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descripcion} - {self.cliente.user.username}"

class Referido(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='referidos_hechos', on_delete=models.CASCADE)
    referido = models.ForeignKey(Cliente, related_name='referidos_recibidos', on_delete=models.CASCADE)
    fecha_referencia = models.DateTimeField(auto_now_add=True)
    puntos_otorgados = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.cliente.user.username} refirió a {self.referido.user.username}"
