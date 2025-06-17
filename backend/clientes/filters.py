import django_filters
from django.db.models import Q
from .models import Cliente, Contacto

class ClienteFilter(django_filters.FilterSet):
    """Filtros para el modelo Cliente"""
    nombre_completo = django_filters.CharFilter(method='filter_nombre_completo')
    localidad = django_filters.CharFilter(lookup_expr='icontains')
    provincia = django_filters.CharFilter(lookup_expr='icontains')
    fecha_registro_desde = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='gte')
    fecha_registro_hasta = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='lte')
    con_compras = django_filters.BooleanFilter(method='filter_con_compras')
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'nombre_completo', 'tipo_documento', 
                  'numero_documento', 'email', 'telefono', 'localidad', 
                  'provincia', 'activo', 'fecha_registro_desde', 'fecha_registro_hasta',
                  'con_compras']
    
    def filter_nombre_completo(self, queryset, name, value):
        """Filtrar por nombre completo (nombre + apellido)"""
        return queryset.filter(
            Q(nombre__icontains=value) | 
            Q(apellido__icontains=value) |
            Q(nombre__icontains=value.split()[0]) & Q(apellido__icontains=value.split()[-1]) if ' ' in value else Q()
        )
    
    def filter_con_compras(self, queryset, name, value):
        """Filtrar clientes que tienen o no compras"""
        if value:  # Si value es True, filtrar clientes con compras
            return queryset.filter(ventas__isnull=False).distinct()
        else:  # Si value es False, filtrar clientes sin compras
            return queryset.filter(ventas__isnull=True)

class ContactoFilter(django_filters.FilterSet):
    """Filtros para el modelo Contacto"""
    cliente_nombre = django_filters.CharFilter(field_name='cliente__nombre', lookup_expr='icontains')
    cliente_apellido = django_filters.CharFilter(field_name='cliente__apellido', lookup_expr='icontains')
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte')
    fecha_seguimiento_desde = django_filters.DateFilter(field_name='fecha_seguimiento', lookup_expr='gte')
    fecha_seguimiento_hasta = django_filters.DateFilter(field_name='fecha_seguimiento', lookup_expr='lte')
    
    class Meta:
        model = Contacto
        fields = ['cliente', 'cliente_nombre', 'cliente_apellido', 'tipo', 
                  'fecha_desde', 'fecha_hasta', 'asunto', 'seguimiento_requerido',
                  'fecha_seguimiento_desde', 'fecha_seguimiento_hasta']