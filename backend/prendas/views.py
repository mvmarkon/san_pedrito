from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from .models import Categoria, Talla, Color, Prenda, VariantePrenda, ImagenPrenda
from .serializers import (
    CategoriaSerializer, 
    TallaSerializer, 
    ColorSerializer, 
    PrendaListSerializer,
    PrendaDetalleSerializer,
    PrendaCreateUpdateSerializer,
    VariantePrendaSerializer,
    VariantePrendaDetalleSerializer,
    VariantePrendaCreateUpdateSerializer,
    ImagenPrendaSerializer,
    ImagenPrendaCreateSerializer
)
from .filters import PrendaFilter, VariantePrendaFilter

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'creado']
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAdminUser()]

class TallaViewSet(viewsets.ModelViewSet):
    queryset = Talla.objects.all()
    serializer_class = TallaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['orden', 'nombre']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class PrendaViewSet(viewsets.ModelViewSet):
    queryset = Prenda.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PrendaFilter
    search_fields = ['nombre', 'descripcion', 'codigo']
    ordering_fields = ['nombre', 'precio_venta', 'creado']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PrendaCreateUpdateSerializer
        elif self.action == 'retrieve':
            return PrendaDetalleSerializer
        return PrendaListSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'buscar']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = Prenda.objects.all()
        
        # Filtrar por stock disponible si se solicita
        stock_disponible = self.request.query_params.get('stock_disponible', None)
        if stock_disponible == 'true':
            queryset = queryset.filter(variantes__stock__gt=0).distinct()
        
        # Filtrar por activo por defecto (a menos que se especifique lo contrario)
        mostrar_inactivos = self.request.query_params.get('mostrar_inactivos', 'false')
        if mostrar_inactivos.lower() != 'true':
            queryset = queryset.filter(activo=True)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Endpoint para búsqueda avanzada de prendas"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Se requiere un término de búsqueda'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) | 
            Q(codigo__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        """Endpoint para obtener prendas con stock bajo"""
        umbral = int(request.query_params.get('umbral', 5))
        
        # Obtener prendas con al menos una variante pero con stock total bajo
        queryset = Prenda.objects.annotate(
            total_stock=Sum('variantes__stock')
        ).filter(
            variantes__isnull=False,
            total_stock__gt=0,
            total_stock__lte=umbral
        ).distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VariantePrendaViewSet(viewsets.ModelViewSet):
    queryset = VariantePrenda.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = VariantePrendaFilter
    ordering_fields = ['prenda__nombre', 'talla__orden', 'color__nombre']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VariantePrendaCreateUpdateSerializer
        elif self.action == 'retrieve':
            return VariantePrendaDetalleSerializer
        return VariantePrendaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = VariantePrenda.objects.all()
        
        # Filtrar por prenda
        prenda_id = self.request.query_params.get('prenda_id', None)
        if prenda_id:
            queryset = queryset.filter(prenda_id=prenda_id)
        
        # Filtrar por stock disponible
        stock_disponible = self.request.query_params.get('stock_disponible', None)
        if stock_disponible == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        # Filtrar por activo por defecto
        mostrar_inactivos = self.request.query_params.get('mostrar_inactivos', 'false')
        if mostrar_inactivos.lower() != 'true':
            queryset = queryset.filter(activo=True)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def ajustar_stock(self, request, pk=None):
        """Endpoint para ajustar el stock de una variante"""
        variante = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        
        try:
            cantidad = int(cantidad)
        except ValueError:
            return Response(
                {'error': 'La cantidad debe ser un número entero'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ajustar el stock
        variante.stock += cantidad
        if variante.stock < 0:
            variante.stock = 0
        variante.save()
        
        serializer = self.get_serializer(variante)
        return Response(serializer.data)

class ImagenPrendaViewSet(viewsets.ModelViewSet):
    queryset = ImagenPrenda.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['orden', 'creado']
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return ImagenPrendaCreateSerializer
        return ImagenPrendaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = ImagenPrenda.objects.all()
        
        # Filtrar por prenda
        prenda_id = self.request.query_params.get('prenda_id', None)
        if prenda_id:
            queryset = queryset.filter(prenda_id=prenda_id)
            
        return queryset