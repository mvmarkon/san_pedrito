from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Contacto

class ContactoInline(admin.TabularInline):
    model = Contacto
    extra = 1
    fields = ('tipo', 'fecha', 'asunto', 'seguimiento_requerido', 'fecha_seguimiento')
    readonly_fields = ('fecha',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo_display', 'telefono', 'email', 'localidad', 'total_compras_display', 'activo')
    list_filter = ('activo', 'localidad', 'provincia', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'telefono', 'numero_documento')
    readonly_fields = ('fecha_registro', 'ultima_actualizacion', 'total_compras', 'monto_total_compras')
    inlines = [ContactoInline]
    fieldsets = (
        ('Información personal', {
            'fields': ('nombre', 'apellido', 'tipo_documento', 'numero_documento', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion', 'localidad', 'provincia', 'codigo_postal')
        }),
        ('Información adicional', {
            'fields': ('notas', 'activo')
        }),
        ('Estadísticas', {
            'fields': ('fecha_registro', 'ultima_actualizacion', 'total_compras', 'monto_total_compras')
        }),
    )
    
    def nombre_completo_display(self, obj):
        return f"{obj.apellido}, {obj.nombre}"
    nombre_completo_display.short_description = 'Nombre completo'
    
    def total_compras_display(self, obj):
        return obj.total_compras
    total_compras_display.short_description = 'Compras'

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('cliente_display', 'tipo', 'fecha', 'asunto', 'seguimiento_display')
    list_filter = ('tipo', 'fecha', 'seguimiento_requerido')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'asunto', 'descripcion')
    readonly_fields = ('fecha',)
    autocomplete_fields = ('cliente',)
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Contacto', {
            'fields': ('tipo', 'fecha', 'asunto', 'descripcion', 'realizado_por')
        }),
        ('Seguimiento', {
            'fields': ('seguimiento_requerido', 'fecha_seguimiento')
        }),
    )
    
    def cliente_display(self, obj):
        return obj.cliente
    cliente_display.short_description = 'Cliente'
    
    def seguimiento_display(self, obj):
        if obj.seguimiento_requerido:
            if obj.fecha_seguimiento:
                return format_html(
                    '<span style="color: {};">Seguimiento: {}</span>',
                    'red' if obj.fecha_seguimiento < obj.fecha.date() else 'green',
                    obj.fecha_seguimiento.strftime('%d/%m/%Y')
                )
            return "Requiere seguimiento"
        return "No requiere"
    seguimiento_display.short_description = 'Seguimiento'