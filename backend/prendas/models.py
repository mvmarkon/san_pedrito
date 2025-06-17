from django.db import models
from django.utils.text import slugify
import uuid

class Categoria(models.Model):
    """Modelo para categorías de prendas (ej. Remeras, Pantalones, etc.)"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre

class Talla(models.Model):
    """Modelo para tallas de prendas (ej. 0-3 meses, 3-6 meses, etc.)"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveSmallIntegerField(default=0, help_text="Orden de visualización")
    
    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre

class Color(models.Model):
    """Modelo para colores de prendas"""
    nombre = models.CharField(max_length=50, unique=True)
    codigo_hex = models.CharField(max_length=7, blank=True, null=True, help_text="Código hexadecimal del color (ej. #FF5733)")
    
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Prenda(models.Model):
    """Modelo principal para prendas de ropa"""
    GENERO_CHOICES = (
        ('N', 'Neutro'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Código único de la prenda")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='prendas')
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de costo en ARS")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de venta en ARS")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='N')
    imagen_principal = models.ImageField(upload_to='prendas/', blank=True, null=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    activo = models.BooleanField(default=True, help_text="Indica si la prenda está disponible para la venta")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prenda"
        verbose_name_plural = "Prendas"
        ordering = ['-creado']
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código único basado en UUID
            self.codigo = str(uuid.uuid4()).split('-')[0].upper()
        
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.codigo}")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    @property
    def stock_total(self):
        """Retorna la suma del stock de todas las variantes de esta prenda"""
        return sum(variante.stock for variante in self.variantes.all())
    
    @property
    def tiene_stock(self):
        """Retorna True si hay al menos una variante con stock disponible"""
        return any(variante.stock > 0 for variante in self.variantes.all())
    
    @property
    def margen_ganancia(self):
        """Calcula el margen de ganancia como porcentaje"""
        if self.precio_costo > 0:
            return ((self.precio_venta - self.precio_costo) / self.precio_costo) * 100
        return 0

class VariantePrenda(models.Model):
    """Modelo para variantes de prendas (combinaciones de talla y color)"""
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, related_name='variantes')
    talla = models.ForeignKey(Talla, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=0)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, unique=True)
    imagen = models.ImageField(upload_to='variantes/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Variante de Prenda"
        verbose_name_plural = "Variantes de Prendas"
        unique_together = ('prenda', 'talla', 'color')
        ordering = ['prenda', 'talla', 'color']
    
    def save(self, *args, **kwargs):
        if not self.codigo_barras:
            # Generar código de barras único
            self.codigo_barras = f"{self.prenda.codigo}-{self.talla.id}-{self.color.id}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.prenda.nombre} - {self.talla.nombre} - {self.color.nombre}"
    
    @property
    def disponible(self):
        """Retorna True si hay stock disponible y la variante está activa"""
        return self.stock > 0 and self.activo

class ImagenPrenda(models.Model):
    """Modelo para imágenes adicionales de prendas"""
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='prendas/')
    titulo = models.CharField(max_length=100, blank=True, null=True)
    orden = models.PositiveSmallIntegerField(default=0, help_text="Orden de visualización")
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Imagen de Prenda"
        verbose_name_plural = "Imágenes de Prendas"
        ordering = ['prenda', 'orden']
    
    def __str__(self):
        return f"Imagen {self.orden} de {self.prenda.nombre}"