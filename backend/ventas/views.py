from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Venta, ItemVenta, Devolucion, ItemDevolucion
from .serializers import (
    VentaListSerializer,
    VentaDetalleSerializer,
    VentaCreateSerializer,
    VentaUpdateSerializer,
    ItemVentaSerializer,
    DevolucionSerializer,
    DevolucionCreateSerializer
)
from .filters import VentaFilter, DevolucionFilter

class VentaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar ventas"""
    queryset = Venta.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VentaFilter
    search_fields = ['numero', 'cliente__nombre', 'cliente__apellido', 'notas']
    ordering_fields = ['fecha', 'total', 'estado']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VentaListSerializer
        elif self.action == 'create':
            return VentaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return VentaUpdateSerializer
        return VentaDetalleSerializer
    
    def get_queryset(self):
        queryset = Venta.objects.all()
        
        # Filtrar por cliente
        cliente_id = self.request.query_params.get('cliente_id', None)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas de ventas"""
        # Obtener parámetros
        periodo = request.query_params.get('periodo', 'mes')
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        
        # Configurar fechas por defecto si no se proporcionan
        hoy = timezone.now().date()
        if not fecha_fin:
            fecha_fin = hoy
        else:
            from datetime import datetime
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        if not fecha_inicio:
            if periodo == 'semana':
                fecha_inicio = hoy - timedelta(days=7)
            elif periodo == 'mes':
                fecha_inicio = hoy.replace(day=1)
            elif periodo == 'anio':
                fecha_inicio = hoy.replace(month=1, day=1)
            else:  # Por defecto, último mes
                fecha_inicio = hoy - timedelta(days=30)
        else:
            from datetime import datetime
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        
        # Filtrar ventas por fecha
        ventas = Venta.objects.filter(
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin,
            estado='PAGADA'  # Solo ventas pagadas
        )
        
        # Calcular estadísticas
        total_ventas = ventas.count()
        monto_total = ventas.aggregate(total=Sum('total'))['total'] or 0
        
        # Ventas por categoría
        from django.db.models import F
        ventas_por_categoria = ItemVenta.objects.filter(
            venta__in=ventas
        ).values(
            categoria=F('variante__prenda__categoria__nombre')
        ).annotate(
            cantidad=Sum('cantidad'),
            monto=Sum('subtotal')
        ).order_by('-monto')
        
        # Productos más vendidos
        productos_mas_vendidos = ItemVenta.objects.filter(
            venta__in=ventas
        ).values(
            'variante__prenda__id',
            'variante__prenda__nombre',
            'variante__prenda__codigo'
        ).annotate(
            cantidad=Sum('cantidad'),
            monto=Sum('subtotal')
        ).order_by('-cantidad')[:10]
        
        # Ventas por día
        from django.db.models.functions import TruncDate
        ventas_por_dia = ventas.annotate(
            dia=TruncDate('fecha')
        ).values('dia').annotate(
            cantidad=Count('id'),
            monto=Sum('total')
        ).order_by('dia')
        
        return Response({
            'periodo': {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
            },
            'resumen': {
                'total_ventas': total_ventas,
                'monto_total': monto_total,
                'ticket_promedio': monto_total / total_ventas if total_ventas > 0 else 0,
            },
            'ventas_por_categoria': ventas_por_categoria,
            'productos_mas_vendidos': productos_mas_vendidos,
            'ventas_por_dia': ventas_por_dia,
        })
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Endpoint para obtener los items de una venta específica"""
        venta = self.get_object()
        items = ItemVenta.objects.filter(venta=venta)
        serializer = ItemVentaSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def devoluciones(self, request, pk=None):
        """Endpoint para obtener las devoluciones de una venta específica"""
        venta = self.get_object()
        devoluciones = Devolucion.objects.filter(venta=venta)
        serializer = DevolucionSerializer(devoluciones, many=True)
        return Response(serializer.data)

class DevolucionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar devoluciones"""
    queryset = Devolucion.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DevolucionFilter
    ordering_fields = ['fecha', 'monto_devuelto']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DevolucionCreateSerializer
        return DevolucionSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.data.get('venta'):
            context['venta_id'] = self.request.data.get('venta')
        return context