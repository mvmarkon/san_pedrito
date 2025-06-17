from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permiso que solo permite acceso a usuarios administradores."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsVendedorUser(permissions.BasePermission):
    """Permiso que solo permite acceso a usuarios vendedores."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_vendedor

class IsInventarioUser(permissions.BasePermission):
    """Permiso que solo permite acceso a usuarios encargados de inventario."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_inventario

class IsAdminOrVendedorUser(permissions.BasePermission):
    """Permiso que permite acceso a usuarios administradores o vendedores."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_admin or request.user.is_vendedor)

class IsAdminOrInventarioUser(permissions.BasePermission):
    """Permiso que permite acceso a usuarios administradores o encargados de inventario."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_admin or request.user.is_inventario)

class IsOwnerOrAdmin(permissions.BasePermission):
    """Permiso que permite a un usuario acceder solo a sus propios recursos o a un administrador acceder a cualquier recurso."""
    
    def has_object_permission(self, request, view, obj):
        # Permitir acceso a administradores
        if request.user and request.user.is_authenticated and request.user.is_admin:
            return True
        
        # Verificar si el objeto tiene un campo 'user' o 'usuario'
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        
        # Si el objeto no tiene un campo 'user' o 'usuario', denegar acceso
        return False