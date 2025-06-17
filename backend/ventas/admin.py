from django.contrib import admin
from django.utils.html import format_html
from .models import Venta, ItemVenta, Devolucion, ItemDevolucion

class ItemVentaInline(admin.TabularInline):
    model = ItemVenta
    extra = 1
    fields = ('variante', 'cantidad', 'precio_unitario', 'descuento_item', 'subtotal')
    readonly_fields = ('subtotal',)
    autocomplete_fields = ('variante',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente_display', 'fecha_display', 'total_display', 'estado_display', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha')
    search_fields = ('numero', 'cliente__nombre', 'cliente__apellido', 'notas')
    readonly_fields = ('numero', 'subtotal', 'total', 'qr_code_display', 'creado', 'actualizado')
    autocomplete_fields = ('cliente',)
    inlines = [ItemVentaInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('numero', 'cliente', 'fecha', 'estado', 'metodo_pago')
        }),
        ('Importes', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total')
        }),
        ('Información adicional', {
            'fields': ('notas', 'vendedor', 'qr_code_display')
        }),
        ('Metadatos', {
            'fields': ('creado', 'actualizado')
        }),
    )
    
    def cliente_display(self, obj):
        return obj.cliente
    cliente_display.short_description = 'Cliente'
    
    def fecha_display(self, obj):
        return obj.fecha.strftime('%d/%m/%Y %H:%M')
    fecha_display.short_description = 'Fecha'
    
    def total_display(self, obj):
        return f"${obj.total}"
    total_display.short_description = 'Total'
    
    def estado_display(self, obj):
        estados_colores = {
            'PENDIENTE': 'orange',
            'PAGADA': 'green',
            'CANCELADA': 'red',
            'DEVUELTA': 'purple'
        }
        color = estados_colores.get(obj.estado, 'black')
        return format_html('<span style="color: {};"><strong>{}</strong></span>', color, obj.get_estado_display())
    estado_display.short_description = 'Estado'
    
    def qr_code_display(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" height="150" />', obj.qr_code.url)
        return "-"
    qr_code_display.short_description = 'Código QR'

class ItemDevolucionInline(admin.TabularInline):
    model = ItemDevolucion
    extra = 1
    fields = ('item_venta', 'cantidad', 'monto')
    autocomplete_fields = ('item_venta',)

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta_display', 'fecha_display', 'motivo_display', 'monto_devuelto_display')
    list_filter = ('motivo', 'fecha')
    search_fields = ('venta__numero', 'venta__cliente__nombre', 'venta__cliente__apellido', 'descripcion')
    readonly_fields = ('venta_link',)
    autocomplete_fields = ('venta',)
    inlines = [ItemDevolucionInline]
    fieldsets = (
        ('Venta', {
            'fields': ('venta', 'venta_link')
        }),
        ('Devolución', {
            'fields': ('fecha', 'motivo', 'descripcion', 'monto_devuelto', 'procesado_por')
        }),
    )
    
    def venta_display(self, obj):
        return f"Venta #{obj.venta.numero}"
    venta_display.short_description = 'Venta'
    
    def fecha_display(self, obj):
        return obj.fecha.strftime('%d/%m/%Y %H:%M')
    fecha_display.short_description = 'Fecha'
    
    def motivo_display(self, obj):
        return obj.get_motivo_display()
    motivo_display.short_description = 'Motivo'
    
    def monto_devuelto_display(self, obj):
        return f"${obj.monto_devuelto}"
    monto_devuelto_display.short_description = 'Monto devuelto'
    
    def venta_link(self, obj):
        if obj.venta:
            return format_html(
                '<a href="{}" target="_blank">Ver detalles de la venta #{}</a>',
                f"/admin/ventas/venta/{obj.venta.id}/change/",
                obj.venta.numero
            )
        return "-"
    venta_link.short_description = 'Enlace a la venta'

@admin.register(ItemVenta)
class ItemVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta_display', 'variante_display', 'cantidad', 'precio_unitario_display', 'subtotal_display')
    list_filter = ('venta__estado',)
    search_fields = ('venta__numero', 'variante__prenda__nombre', 'variante__prenda__codigo')
    readonly_fields = ('subtotal',)
    autocomplete_fields = ('venta', 'variante')
    
    def venta_display(self, obj):
        return f"Venta #{obj.venta.numero}"
    venta_display.short_description = 'Venta'
    
    def variante_display(self, obj):
        return f"{obj.variante.prenda.nombre} - {obj.variante.talla.nombre} - {obj.variante.color.nombre}"
    variante_display.short_description = 'Variante'
    
    def precio_unitario_display(self, obj):
        return f"${obj.precio_unitario}"
    precio_unitario_display.short_description = 'Precio unitario'
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal}"
    subtotal_display.short_description = 'Subtotal'

@admin.register(ItemDevolucion)
class ItemDevolucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'devolucion_display', 'item_venta_display', 'cantidad', 'monto_display')
    list_filter = ('devolucion__motivo',)
    search_fields = ('devolucion__venta__numero', 'item_venta__variante__prenda__nombre')
    autocomplete_fields = ('devolucion', 'item_venta')
    
    def devolucion_display(self, obj):
        return f"Devolución de Venta #{obj.devolucion.venta.numero}"
    devolucion_display.short_description = 'Devolución'
    
    def item_venta_display(self, obj):
        return f"{obj.item_venta.variante.prenda.nombre} - {obj.item_venta.variante.talla.nombre} - {obj.item_venta.variante.color.nombre}"
    item_venta_display.short_description = 'Item devuelto'
    
    def monto_display(self, obj):
        return f"${obj.monto}"
    monto_display.short_description = 'Monto'