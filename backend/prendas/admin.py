from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Talla, Color, Prenda, VariantePrenda, ImagenPrenda

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'creado', 'actualizado')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('creado', 'actualizado')

@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    search_fields = ('nombre',)
    list_editable = ('orden',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'muestra_color')
    search_fields = ('nombre',)
    
    def muestra_color(self, obj):
        if obj.codigo_hex:
            return format_html(
                '<div style="background-color: {}; width: 30px; height: 15px;"></div>',
                obj.codigo_hex
            )
        return "-"
    muestra_color.short_description = 'Color'

class VariantePrendaInline(admin.TabularInline):
    model = VariantePrenda
    extra = 1
    fields = ('talla', 'color', 'stock', 'codigo_barras', 'activo')
    readonly_fields = ('codigo_barras',)

class ImagenPrendaInline(admin.TabularInline):
    model = ImagenPrenda
    extra = 1
    fields = ('imagen', 'titulo', 'orden')

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio_venta', 'stock_total', 'tiene_stock', 'activo')
    list_filter = ('categoria', 'genero', 'activo')
    search_fields = ('nombre', 'codigo', 'descripcion')
    readonly_fields = ('codigo', 'slug', 'creado', 'actualizado', 'stock_total', 'tiene_stock', 'margen_ganancia')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [VariantePrendaInline, ImagenPrendaInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('codigo', 'nombre', 'slug', 'descripcion', 'categoria', 'genero', 'activo')
        }),
        ('Precios', {
            'fields': ('precio_costo', 'precio_venta', 'margen_ganancia')
        }),
        ('Imagen', {
            'fields': ('imagen_principal',)
        }),
        ('Información adicional', {
            'fields': ('stock_total', 'tiene_stock', 'creado', 'actualizado')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Edición
            return self.readonly_fields
        return ('creado', 'actualizado', 'stock_total', 'tiene_stock', 'margen_ganancia')  # Creación

@admin.register(VariantePrenda)
class VariantePrendaAdmin(admin.ModelAdmin):
    list_display = ('prenda', 'talla', 'color', 'stock', 'codigo_barras', 'disponible', 'activo')
    list_filter = ('prenda__categoria', 'talla', 'color', 'activo')
    search_fields = ('prenda__nombre', 'prenda__codigo', 'codigo_barras')
    readonly_fields = ('codigo_barras', 'creado', 'actualizado')
    list_editable = ('stock', 'activo')
    autocomplete_fields = ('prenda', 'talla', 'color')

@admin.register(ImagenPrenda)
class ImagenPrendaAdmin(admin.ModelAdmin):
    list_display = ('prenda', 'titulo', 'orden', 'miniatura')
    list_filter = ('prenda__categoria',)
    search_fields = ('prenda__nombre', 'titulo')
    list_editable = ('orden',)
    autocomplete_fields = ('prenda',)
    
    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" height="50" />', obj.imagen.url)
        return "-"
    miniatura.short_description = 'Imagen'