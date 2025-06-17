from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from clientes.models import Cliente
from prendas.models import VariantePrenda
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Venta(models.Model):
    """Modelo para registrar ventas de prendas"""
    ESTADO_CHOICES = (
        ('PENDIENTE', 'Pendiente de pago'),
        ('PAGADA', 'Pagada'),
        ('CANCELADA', 'Cancelada'),
        ('DEVUELTA', 'Devuelta'),
    )
    
    METODO_PAGO_CHOICES = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_CREDITO', 'Tarjeta de Crédito'),
        ('TARJETA_DEBITO', 'Tarjeta de Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('MERCADO_PAGO', 'Mercado Pago'),
        ('OTRO', 'Otro'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Número de venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='EFECTIVO')
    notas = models.TextField(blank=True, null=True)
    vendedor = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre del vendedor")
    qr_code = models.ImageField(upload_to='ventas/qr_codes/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['cliente']),
            models.Index(fields=['fecha']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"Venta #{self.numero} - {self.cliente.nombre_completo}"
    
    def save(self, *args, **kwargs):
        # Generar número de venta si no existe
        if not self.numero:
            ultimo_numero = Venta.objects.all().order_by('-creado').values_list('numero', flat=True).first()
            if ultimo_numero and ultimo_numero.isdigit():
                self.numero = str(int(ultimo_numero) + 1).zfill(8)
            else:
                self.numero = '00000001'
        
        # Calcular total si no se ha establecido
        if not self.total:
            self.total = self.subtotal - self.descuento + self.impuestos
        
        # Generar código QR si no existe
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"VENTA:{self.id}|NUMERO:{self.numero}|CLIENTE:{self.cliente.id}|FECHA:{self.fecha}|TOTAL:{self.total}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_code.save(f"venta_{self.numero}_qr.png", File(buffer), save=False)
        
        super().save(*args, **kwargs)
    
    @property
    def cantidad_items(self):
        """Retorna la cantidad total de items en la venta"""
        return sum(item.cantidad for item in self.items.all())
    
    @property
    def esta_pagada(self):
        """Retorna True si la venta está pagada"""
        return self.estado == 'PAGADA'

class ItemVenta(models.Model):
    """Modelo para items individuales dentro de una venta"""
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    variante = models.ForeignKey(VariantePrenda, on_delete=models.PROTECT, related_name='ventas')
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descuento_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"
        ordering = ['id']
        unique_together = ('venta', 'variante')
    
    def __str__(self):
        return f"{self.cantidad} x {self.variante} (${self.precio_unitario})"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal si no se ha establecido
        if not self.subtotal:
            self.subtotal = (self.precio_unitario * self.cantidad) - self.descuento_item
        
        super().save(*args, **kwargs)
        
        # Actualizar totales de la venta
        self.actualizar_totales_venta()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        
        # Actualizar totales de la venta
        self.actualizar_totales_venta()
    
    def actualizar_totales_venta(self):
        """Actualiza los totales de la venta asociada"""
        venta = self.venta
        items = venta.items.all()
        
        # Calcular subtotal sumando los subtotales de todos los items
        subtotal = sum(item.subtotal for item in items)
        
        # Actualizar venta
        venta.subtotal = subtotal
        venta.total = subtotal - venta.descuento + venta.impuestos
        venta.save()

class Devolucion(models.Model):
    """Modelo para registrar devoluciones de ventas"""
    MOTIVO_CHOICES = (
        ('DEFECTO', 'Producto defectuoso'),
        ('TALLA', 'Talla incorrecta'),
        ('COLOR', 'Color incorrecto'),
        ('ARREPENTIMIENTO', 'Arrepentimiento de compra'),
        ('OTRO', 'Otro motivo'),
    )
    
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name='devoluciones')
    fecha = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    monto_devuelto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    procesado_por = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre de quien procesó la devolución")
    
    class Meta:
        verbose_name = "Devolución"
        verbose_name_plural = "Devoluciones"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Devolución de Venta #{self.venta.numero} - {self.get_motivo_display()}"
    
    def save(self, *args, **kwargs):
        # Si es una nueva devolución, actualizar el estado de la venta
        if not self.pk:
            self.venta.estado = 'DEVUELTA'
            self.venta.save()
        
        super().save(*args, **kwargs)

class ItemDevolucion(models.Model):
    """Modelo para items individuales dentro de una devolución"""
    devolucion = models.ForeignKey(Devolucion, on_delete=models.CASCADE, related_name='items')
    item_venta = models.ForeignKey(ItemVenta, on_delete=models.PROTECT, related_name='devoluciones')
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Item de Devolución"
        verbose_name_plural = "Items de Devolución"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.cantidad} x {self.item_venta.variante}"
    
    def save(self, *args, **kwargs):
        # Validar que la cantidad a devolver no exceda la cantidad vendida
        if self.cantidad > self.item_venta.cantidad:
            raise ValueError("La cantidad a devolver no puede exceder la cantidad vendida")
        
        # Si es un nuevo item, actualizar el stock
        if not self.pk:
            # Devolver stock
            variante = self.item_venta.variante
            variante.stock += self.cantidad
            variante.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Restar stock al eliminar una devolución
        variante = self.item_venta.variante
        variante.stock -= self.cantidad
        variante.save()
        
        super().delete(*args, **kwargs)