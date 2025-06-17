import django_filters
from django.db.models import Q
from .models import Venta, Devolucion

class VentaFilter(django_filters.FilterSet):
    """Filtros para el modelo Venta"""
    cliente_nombre = django_filters.CharFilter(method='filter_cliente_nombre')
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='date__gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='date__lte')
    total_min = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_max = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    
    class Meta:
        model = Venta
        fields = ['numero', 'cliente', 'cliente_nombre', 'fecha_desde', 'fecha_hasta', 
                  'estado', 'metodo_pago', 'total_min', 'total_max']
    
    def filter_cliente_nombre(self, queryset, name, value):
        """Filtrar por nombre o apellido del cliente"""
        return queryset.filter(
            Q(cliente__nombre__icontains=value) | 
            Q(cliente__apellido__icontains=value)
        )

class DevolucionFilter(django_filters.FilterSet):
    """Filtros para el modelo Devolucion"""
    venta_numero = django_filters.CharFilter(field_name='venta__numero', lookup_expr='icontains')
    cliente = django_filters.CharFilter(method='filter_cliente')
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='date__gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='date__lte')
    monto_min = django_filters.NumberFilter(field_name='monto_devuelto', lookup_expr='gte')
    monto_max = django_filters.NumberFilter(field_name='monto_devuelto', lookup_expr='lte')
    
    class Meta:
        model = Devolucion
        fields = ['venta', 'venta_numero', 'cliente', 'fecha_desde', 'fecha_hasta', 
                  'motivo', 'monto_min', 'monto_max']
    
    def filter_cliente(self, queryset, name, value):
        """Filtrar por nombre o apellido del cliente de la venta"""
        return queryset.filter(
            Q(venta__cliente__nombre__icontains=value) | 
            Q(venta__cliente__apellido__icontains=value)
        )