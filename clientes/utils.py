from django.db.models import Sum
from .models import Punto

def calcular_nivel(cliente):
    """Calcula y actualiza el nivel del cliente según sus puntos totales"""
    total = Punto.objects.filter(cliente=cliente).aggregate(Sum('puntos_obtenidos'))['puntos_obtenidos__sum'] or 0
    if total >= 5000:
        cliente.nivel = 'Oro'
    elif total >= 2000:
        cliente.nivel = 'Plata'
    else:
        cliente.nivel = 'Bronce'
    cliente.save()
    return total
