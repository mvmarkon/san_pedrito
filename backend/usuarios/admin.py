from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nombre_completo', 'rol_display', 'is_active', 'is_staff', 'ultimo_acceso')
    list_filter = ('rol', 'is_active', 'is_staff', 'is_superuser', 'creado')
    search_fields = ('email', 'nombre', 'apellido', 'telefono')
    ordering = ('apellido', 'nombre')
    readonly_fields = ('ultimo_acceso', 'creado', 'actualizado', 'foto_preview')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('nombre', 'apellido', 'telefono', 'foto', 'foto_preview')}),
        (_('Permisos'), {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('ultimo_acceso', 'date_joined', 'creado', 'actualizado')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre', 'apellido', 'rol', 'is_active', 'is_staff'),
        }),
    )
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Nombre completo'
    
    def rol_display(self, obj):
        roles_colores = {
            'ADMIN': 'red',
            'VENDEDOR': 'green',
            'INVENTARIO': 'blue'
        }
        color = roles_colores.get(obj.rol, 'black')
        return format_html('<span style="color: {};"><strong>{}</strong></span>', color, obj.get_rol_display())
    rol_display.short_description = 'Rol'
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" height="150" />', obj.foto.url)
        return "-"
    foto_preview.short_description = 'Vista previa de la foto'