from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from .models import Cliente, Contacto
from .serializers import (
    ClienteListSerializer,
    ClienteDetailSerializer,
    ClienteCreateUpdateSerializer,
    ContactoSerializer,
    ContactoCreateSerializer
)
from .filters import ClienteFilter, ContactoFilter

class ClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clientes"""
    queryset = Cliente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClienteFilter
    search_fields = ['nombre', 'apellido', 'email', 'telefono', 'numero_documento']
    ordering_fields = ['apellido', 'nombre', 'fecha_registro', 'ultima_actualizacion']
    ordering = ['apellido', 'nombre']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClienteCreateUpdateSerializer
        return ClienteDetailSerializer
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        
        # Filtrar por activo por defecto (a menos que se especifique lo contrario)
        mostrar_inactivos = self.request.query_params.get('mostrar_inactivos', 'false')
        if mostrar_inactivos.lower() != 'true':
            queryset = queryset.filter(activo=True)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Endpoint para búsqueda avanzada de clientes"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Se requiere un término de búsqueda'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(email__icontains=query) |
            Q(telefono__icontains=query) |
            Q(numero_documento__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mejores_clientes(self, request):
        """Endpoint para obtener los mejores clientes por monto de compras"""
        limite = int(request.query_params.get('limite', 10))
        
        # Obtener clientes con sus montos totales de compra
        queryset = Cliente.objects.annotate(
            total_ventas=Count('ventas'),
            monto_total=Sum('ventas__total')
        ).filter(
            total_ventas__gt=0
        ).order_by('-monto_total')[:limite]
        
        serializer = ClienteListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def contactos(self, request, pk=None):
        """Endpoint para obtener los contactos de un cliente específico"""
        cliente = self.get_object()
        contactos = Contacto.objects.filter(cliente=cliente)
        
        # Aplicar filtros si existen
        tipo = request.query_params.get('tipo', None)
        if tipo:
            contactos = contactos.filter(tipo=tipo)
            
        seguimiento = request.query_params.get('seguimiento', None)
        if seguimiento == 'true':
            contactos = contactos.filter(seguimiento_requerido=True)
        elif seguimiento == 'false':
            contactos = contactos.filter(seguimiento_requerido=False)
        
        serializer = ContactoSerializer(contactos, many=True)
        return Response(serializer.data)

class ContactoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar contactos con clientes"""
    queryset = Contacto.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContactoFilter
    search_fields = ['asunto', 'descripcion', 'cliente__nombre', 'cliente__apellido']
    ordering_fields = ['fecha', 'tipo', 'seguimiento_requerido', 'fecha_seguimiento']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactoCreateSerializer
        return ContactoSerializer
    
    def get_queryset(self):
        queryset = Contacto.objects.all()
        
        # Filtrar por cliente
        cliente_id = self.request.query_params.get('cliente_id', None)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        # Filtrar por seguimiento pendiente
        seguimiento_pendiente = self.request.query_params.get('seguimiento_pendiente', None)
        if seguimiento_pendiente == 'true':
            from django.utils import timezone
            today = timezone.now().date()
            queryset = queryset.filter(
                seguimiento_requerido=True,
                fecha_seguimiento__gte=today
            )
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def pendientes_seguimiento(self, request):
        """Endpoint para obtener contactos que requieren seguimiento"""
        from django.utils import timezone
        today = timezone.now().date()
        
        queryset = Contacto.objects.filter(
            seguimiento_requerido=True,
            fecha_seguimiento__lte=today
        ).order_by('fecha_seguimiento')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)