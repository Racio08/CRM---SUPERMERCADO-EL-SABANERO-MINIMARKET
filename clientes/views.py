from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Cliente, Factura, Punto, Campana, Premio
from .utils import calcular_nivel
from .forms import ClienteRegistroForm

# VISTAS CLIENTE
@login_required
def registrar_factura(request):
    if request.method == 'POST':
        numero = request.POST['numero_factura']
        fecha = request.POST['fecha_compra']
        valor = float(request.POST['valor_total'])
        sucursal = request.POST['sucursal']
        
        # Verificar si el usuario tiene un cliente asociado
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            messages.error(request, "No tienes un perfil de cliente asociado.")
            return redirect('clientes:home')

        factura = Factura.objects.create(
            cliente=cliente,
            numero_factura=numero,
            fecha_compra=fecha,
            valor_total=valor,
            sucursal=sucursal,
            registrada=True
        )

        hoy = now().date()
        campanas_activas = Campana.objects.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy)
        
        multiplicador = 1.0
        if campanas_activas.exists():
            ultima_campana = campanas_activas.last()
            if ultima_campana:
                multiplicador = ultima_campana.multiplicador_puntos

        puntos = int((valor // 1000) * multiplicador)
        Punto.objects.create(
            cliente=cliente,
            factura=factura,
            puntos_obtenidos=puntos,
            tipo='Compra'
        )

        calcular_nivel(cliente)
        messages.success(request, f"Factura registrada con {puntos} puntos.")
        return redirect('clientes:ver_puntos')

    return render(request, 'clientes/registrar_factura.html')

@login_required
def ver_puntos(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, "No tienes un perfil de cliente asociado.")
        return redirect('clientes:home')
    
    total = Punto.objects.filter(cliente=cliente).aggregate(Sum('puntos_obtenidos'))['puntos_obtenidos__sum'] or 0
    premios = Premio.objects.filter(cliente=cliente)
    historial_puntos = Punto.objects.filter(cliente=cliente).order_by('-fecha_obtencion')[:10]
    
    return render(request, 'clientes/ver_puntos.html', {
        'total_puntos': total, 
        'nivel': cliente.nivel, 
        'premios': premios,
        'historial': historial_puntos
    })

@login_required
def ranking_mensual(request):
    mes_actual = now().month
    ranking = Punto.objects.filter(fecha_obtencion__month=mes_actual).values('cliente__user__username').annotate(
        total=Sum('puntos_obtenidos')).order_by('-total')[:10]
    return render(request, 'clientes/ranking.html', {'ranking': ranking})

# VISTAS ADMINISTRADOR
@login_required
def panel_admin(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('clientes:home')
    
    clientes = Cliente.objects.annotate(puntos=Sum('punto__puntos_obtenidos')).order_by('-puntos')
    facturas = Factura.objects.select_related('cliente').order_by('-fecha_compra')[:10]
    campanas = Campana.objects.all()
    
    return render(request, 'clientes/admin/panel.html', {
        'clientes': clientes, 
        'facturas': facturas, 
        'campanas': campanas
    })

# Vista de inicio
def home(request):
    return render(request, 'clientes/home.html')

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            # Crear usuario
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Crear cliente
            cliente = form.save(commit=False)
            cliente.user = user
            cliente.save()
            
            # Login automático
            login(request, user)
            
            messages.success(request, f'¡Bienvenido {user.first_name}! Tu cuenta ha sido creada exitosamente.')
            return redirect('clientes:ver_puntos')
    else:
        form = ClienteRegistroForm()
    
    return render(request, 'clientes/registro.html', {'form': form})

# Vista de logout
def salir(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('clientes:home')
