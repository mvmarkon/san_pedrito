import django_filters
from .models import Prenda, VariantePrenda

class PrendaFilter(django_filters.FilterSet):
    """Filtros para el modelo Prenda"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.NumberFilter(field_name='categoria__id')
    categoria_slug = django_filters.CharFilter(field_name='categoria__slug')
    precio_min = django_filters.NumberFilter(field_name='precio_venta', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_venta', lookup_expr='lte')
    genero = django_filters.CharFilter()
    tiene_stock = django_filters.BooleanFilter(method='filter_tiene_stock')
    talla = django_filters.NumberFilter(method='filter_talla')
    color = django_filters.NumberFilter(method='filter_color')
    
    class Meta:
        model = Prenda
        fields = ['nombre', 'categoria', 'categoria_slug', 'precio_min', 'precio_max', 
                  'genero', 'tiene_stock', 'talla', 'color', 'activo']
    
    def filter_tiene_stock(self, queryset, name, value):
        """Filtrar prendas que tienen o no stock"""
        if value:  # Si value es True, filtrar prendas con stock
            return queryset.filter(variantes__stock__gt=0).distinct()
        else:  # Si value es False, filtrar prendas sin stock
            return queryset.exclude(variantes__stock__gt=0).distinct()
    
    def filter_talla(self, queryset, name, value):
        """Filtrar prendas por talla"""
        return queryset.filter(variantes__talla_id=value).distinct()
    
    def filter_color(self, queryset, name, value):
        """Filtrar prendas por color"""
        return queryset.filter(variantes__color_id=value).distinct()

class VariantePrendaFilter(django_filters.FilterSet):
    """Filtros para el modelo VariantePrenda"""
    prenda = django_filters.NumberFilter(field_name='prenda__id')
    prenda_slug = django_filters.CharFilter(field_name='prenda__slug')
    talla = django_filters.NumberFilter(field_name='talla__id')
    color = django_filters.NumberFilter(field_name='color__id')
    disponible = django_filters.BooleanFilter(method='filter_disponible')
    
    class Meta:
        model = VariantePrenda
        fields = ['prenda', 'prenda_slug', 'talla', 'color', 'disponible', 'activo']
    
    def filter_disponible(self, queryset, name, value):
        """Filtrar variantes disponibles (con stock y activas)"""
        if value:  # Si value es True, filtrar variantes disponibles
            return queryset.filter(stock__gt=0, activo=True)
        else:  # Si value es False, filtrar variantes no disponibles
            return queryset.filter(stock=0) | queryset.filter(activo=False)