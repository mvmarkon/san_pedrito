from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UsuarioListSerializer, 
    UsuarioDetailSerializer, 
    UsuarioCreateSerializer, 
    UsuarioUpdateSerializer,
    CambiarPasswordSerializer,
    PerfilUsuarioSerializer
)

Usuario = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso personalizado para permitir solo a administradores crear, actualizar o eliminar usuarios."""
    
    def has_permission(self, request, view):
        # Permitir GET, HEAD u OPTIONS a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Permitir POST, PUT, PATCH, DELETE solo a administradores
        return request.user and request.user.is_authenticated and request.user.is_admin

class UsuarioViewSet(viewsets.ModelViewSet):
    """API para gestionar usuarios"""
    queryset = Usuario.objects.all().order_by('apellido', 'nombre')
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UsuarioUpdateSerializer
        elif self.action == 'retrieve':
            return UsuarioDetailSerializer
        elif self.action == 'cambiar_password':
            return CambiarPasswordSerializer
        elif self.action == 'perfil':
            return PerfilUsuarioSerializer
        return UsuarioListSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_password(self, request, pk=None):
        """Cambiar la contraseña de un usuario"""
        user = self.get_object()
        
        # Solo permitir al propio usuario o a un administrador cambiar la contraseña
        if request.user.id != user.id and not request.user.is_admin:
            return Response(
                {"detail": "No tienes permiso para cambiar la contraseña de este usuario."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Contraseña cambiada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def perfil(self, request):
        """Obtener o actualizar el perfil del usuario autenticado"""
        user = request.user
        
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def vendedores(self, request):
        """Obtener lista de usuarios con rol de vendedor"""
        vendedores = Usuario.objects.filter(rol='VENDEDOR', is_active=True).order_by('apellido', 'nombre')
        serializer = UsuarioListSerializer(vendedores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Invalidar el token de refresco del usuario"""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Actualizar último acceso
            user = request.user
            user.ultimo_acceso = timezone.now()
            user.save(update_fields=['ultimo_acceso'])
            
            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)