from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.contrib import messages


# MODELOS
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    nivel = models.CharField(max_length=10, default="Bronce")
    fecha_registro = models.DateTimeField(auto_now_add=True)


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50)
    fecha_compra = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    sucursal = models.CharField(max_length=100)
    registrada = models.BooleanField(default=False)


class Punto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, null=True, blank=True
    )
    puntos_obtenidos = models.IntegerField()
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, default="Compra")


class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    multiplicador_puntos = models.FloatField(default=1.0)


class Premio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    puntos_requeridos = models.IntegerField()
    fecha_otorgado = models.DateField(auto_now_add=True)
    entregado = models.BooleanField(default=False)


class Referido(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name="referente", on_delete=models.CASCADE
    )
    referido = models.ForeignKey(
        Cliente, related_name="referido", on_delete=models.CASCADE
    )
    fecha_referencia = models.DateTimeField(auto_now_add=True)
    puntos_otorgados = models.IntegerField(default=0)


# UTILIDADES


def calcular_nivel(cliente):
    total = (
        Punto.objects.filter(cliente=cliente).aggregate(Sum("puntos_obtenidos"))[
            "puntos_obtenidos__sum"
        ]
        or 0
    )
    if total >= 5000:
        cliente.nivel = "Oro"
    elif total >= 2000:
        cliente.nivel = "Plata"
    else:
        cliente.nivel = "Bronce"
    cliente.save()


# VISTAS CLIENTE
@login_required
def registrar_factura(request):
    if request.method == "POST":
        numero = request.POST["numero_factura"]
        fecha = request.POST["fecha_compra"]
        valor = float(request.POST["valor_total"])
        sucursal = request.POST["sucursal"]
        cliente = request.user.cliente

        factura = Factura.objects.create(
            cliente=cliente,
            numero_factura=numero,
            fecha_compra=fecha,
            valor_total=valor,
            sucursal=sucursal,
            registrada=True,
        )

        hoy = now().date()
        campanas_activas = Campana.objects.filter(
            fecha_inicio__lte=hoy, fecha_fin__gte=hoy
        )
        multiplicador = (
            campanas_activas.last().multiplicador_puntos
            if campanas_activas.exists()
            else 1.0
        )

        puntos = int((valor // 1000) * multiplicador)
        Punto.objects.create(
            cliente=cliente, factura=factura, puntos_obtenidos=puntos, tipo="Compra"
        )

        calcular_nivel(cliente)
        messages.success(request, f"Factura registrada con {puntos} puntos.")
        return redirect("ver_puntos")

    return render(request, "registrar_factura.html")


@login_required
def ver_puntos(request):
    cliente = request.user.cliente
    total = (
        Punto.objects.filter(cliente=cliente).aggregate(Sum("puntos_obtenidos"))[
            "puntos_obtenidos__sum"
        ]
        or 0
    )
    premios = Premio.objects.filter(cliente=cliente)
    return render(
        request,
        "ver_puntos.html",
        {"total_puntos": total, "nivel": cliente.nivel, "premios": premios},
    )


@login_required
def ranking_mensual(request):
    mes_actual = now().month
    ranking = (
        Punto.objects.filter(fecha_obtencion__month=mes_actual)
        .values("cliente__user__username")
        .annotate(total=Sum("puntos_obtenidos"))
        .order_by("-total")[:10]
    )
    return render(request, "ranking.html", {"ranking": ranking})


# VISTAS ADMINISTRADOR
@login_required
def panel_admin(request):
    if not request.user.is_staff:
        return redirect("home")
    clientes = Cliente.objects.annotate(puntos=Sum("punto__puntos_obtenidos")).order_by(
        "-puntos"
    )
    facturas = Factura.objects.select_related("cliente").order_by("-fecha_compra")[:10]
    campanas = Campana.objects.all()
    return render(
        request,
        "admin/panel.html",
        {"clientes": clientes, "facturas": facturas, "campanas": campanas},
    )
