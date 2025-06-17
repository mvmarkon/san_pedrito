from django.db import models
from django.core.validators import RegexValidator
import uuid

class Cliente(models.Model):
    """Modelo para almacenar información de clientes"""
    TIPO_DOCUMENTO_CHOICES = (
        ('DNI', 'DNI'),
        ('CUIT', 'CUIT'),
        ('PASAPORTE', 'Pasaporte'),
        ('OTRO', 'Otro'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, default='DNI')
    numero_documento = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    telefono = models.CharField(validators=[telefono_regex], max_length=17, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
        indexes = [
            models.Index(fields=['apellido', 'nombre']),
            models.Index(fields=['numero_documento']),
            models.Index(fields=['email']),
            models.Index(fields=['telefono']),
        ]
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def total_compras(self):
        """Retorna el total de compras realizadas por el cliente"""
        return self.ventas.count()
    
    @property
    def monto_total_compras(self):
        """Retorna el monto total de compras realizadas por el cliente"""
        from django.db.models import Sum
        return self.ventas.aggregate(total=Sum('total'))['total'] or 0

class Contacto(models.Model):
    """Modelo para registrar interacciones con clientes"""
    TIPO_CONTACTO_CHOICES = (
        ('LLAMADA', 'Llamada telefónica'),
        ('EMAIL', 'Correo electrónico'),
        ('WHATSAPP', 'WhatsApp'),
        ('PRESENCIAL', 'Visita presencial'),
        ('OTRO', 'Otro'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contactos')
    tipo = models.CharField(max_length=20, choices=TIPO_CONTACTO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    realizado_por = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre de la persona que realizó el contacto")
    seguimiento_requerido = models.BooleanField(default=False)
    fecha_seguimiento = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.get_tipo_display()} con {self.cliente} - {self.fecha.strftime('%d/%m/%Y')}"