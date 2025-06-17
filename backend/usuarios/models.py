from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el email y contraseña dados."""
        if not email:
            raise ValueError(_('El email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('rol', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Modelo de usuario personalizado que utiliza email como identificador único."""
    
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Vendedor'),
        ('INVENTARIO', 'Encargado de Inventario'),
    )
    
    username = None
    email = models.EmailField(_('dirección de email'), unique=True)
    nombre = models.CharField(_('nombre'), max_length=150)
    apellido = models.CharField(_('apellido'), max_length=150)
    rol = models.CharField(_('rol'), max_length=20, choices=ROLES, default='VENDEDOR')
    telefono = models.CharField(
        _('teléfono'), 
        max_length=15, 
        validators=[RegexValidator(r'^\+?[0-9]{8,15}$', 'Ingrese un número de teléfono válido.')],
        blank=True
    )
    foto = models.ImageField(_('foto de perfil'), upload_to='usuarios/fotos/', blank=True, null=True)
    ultimo_acceso = models.DateTimeField(_('último acceso'), blank=True, null=True)
    activo = models.BooleanField(_('activo'), default=True)
    creado = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    actualizado = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.nombre} {self.apellido}"
    
    def get_short_name(self):
        """Retorna el nombre del usuario."""
        return self.nombre
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador."""
        return self.rol == 'ADMIN'
    
    @property
    def is_vendedor(self):
        """Verifica si el usuario es vendedor."""
        return self.rol == 'VENDEDOR'
    
    @property
    def is_inventario(self):
        """Verifica si el usuario es encargado de inventario."""
        return self.rol == 'INVENTARIO'