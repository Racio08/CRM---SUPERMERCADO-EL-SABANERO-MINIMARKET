from django.contrib import admin
from .models import Cliente, Factura, Punto, Campana, Premio, Referido, CatalogoPremio

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'numero_documento', 'telefono', 'ciudad', 'nivel', 'activo', 'fecha_registro')
    list_filter = ('nivel', 'activo', 'ciudad', 'tipo_documento', 'genero', 'acepta_promociones')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'numero_documento', 'telefono')
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Identificación', {
            'fields': ('tipo_documento', 'numero_documento')
        }),
        ('Información Personal', {
            'fields': ('fecha_nacimiento', 'genero')
        }),
        ('Contacto', {
            'fields': ('telefono', 'telefono_alternativo', 'email_alternativo')
        }),
        ('Dirección', {
            'fields': ('direccion', 'barrio', 'ciudad', 'departamento', 'codigo_postal')
        }),
        ('CRM', {
            'fields': ('nivel', 'activo', 'fecha_registro')
        }),
        ('Referidos', {
            'fields': ('codigo_referido', 'referido_por')
        }),
        ('Preferencias', {
            'fields': ('acepta_promociones', 'acepta_notificaciones')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_nombre_completo.short_description = 'Nombre Completo'

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'fecha_compra', 'valor_total', 'sucursal', 'registrada')
    list_filter = ('registrada', 'fecha_compra', 'sucursal')
    search_fields = ('numero_factura', 'cliente__user__username')
    date_hierarchy = 'fecha_compra'

@admin.register(Punto)
class PuntoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'puntos_obtenidos', 'tipo', 'fecha_obtencion', 'factura')
    list_filter = ('tipo', 'fecha_obtencion')
    search_fields = ('cliente__user__username',)
    date_hierarchy = 'fecha_obtencion'

@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'multiplicador_puntos')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('nombre', 'descripcion')

@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'cliente', 'puntos_requeridos', 'fecha_otorgado', 'entregado')
    list_filter = ('entregado', 'fecha_otorgado')
    search_fields = ('descripcion', 'cliente__user__username')

@admin.register(Referido)
class ReferidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'referido', 'fecha_referencia', 'puntos_otorgados')
    list_filter = ('fecha_referencia',)
    search_fields = ('cliente__user__username', 'referido__user__username')

@admin.register(CatalogoPremio)
class CatalogoPremioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos_requeridos', 'disponible', 'stock')
    list_filter = ('disponible', 'puntos_requeridos')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('disponible', 'stock')
    ordering = ('puntos_requeridos',)
