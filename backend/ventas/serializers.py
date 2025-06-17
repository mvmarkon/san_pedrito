from rest_framework import serializers
from django.db import transaction
from .models import Venta, ItemVenta, Devolucion, ItemDevolucion
from clientes.models import Cliente
from clientes.serializers import ClienteListSerializer
from prendas.models import VariantePrenda
from prendas.serializers import VariantePrendaSerializer

class ItemVentaSerializer(serializers.ModelSerializer):
    """Serializador para items de venta con información básica"""
    variante_nombre = serializers.ReadOnlyField(source='variante.prenda.nombre')
    variante_talla = serializers.ReadOnlyField(source='variante.talla.nombre')
    variante_color = serializers.ReadOnlyField(source='variante.color.nombre')
    
    class Meta:
        model = ItemVenta
        fields = ['id', 'variante', 'variante_nombre', 'variante_talla', 'variante_color',
                  'cantidad', 'precio_unitario', 'descuento_item', 'subtotal']
        read_only_fields = ['id', 'subtotal', 'variante_nombre', 'variante_talla', 'variante_color']

class ItemVentaDetalleSerializer(ItemVentaSerializer):
    """Serializador para detalles completos de items de venta"""
    variante = VariantePrendaSerializer(read_only=True)

class VentaListSerializer(serializers.ModelSerializer):
    """Serializador para listar ventas con información básica"""
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre_completo')
    cantidad_items = serializers.ReadOnlyField()
    
    class Meta:
        model = Venta
        fields = ['id', 'numero', 'cliente', 'cliente_nombre', 'fecha', 
                  'total', 'estado', 'metodo_pago', 'cantidad_items']
        read_only_fields = ['id', 'numero', 'cantidad_items']

class VentaDetalleSerializer(serializers.ModelSerializer):
    """Serializador para ver detalles completos de una venta"""
    cliente = ClienteListSerializer(read_only=True)
    items = ItemVentaDetalleSerializer(many=True, read_only=True)
    cantidad_items = serializers.ReadOnlyField()
    
    class Meta:
        model = Venta
        fields = ['id', 'numero', 'cliente', 'fecha', 'subtotal', 'descuento', 
                  'impuestos', 'total', 'estado', 'metodo_pago', 'notas', 
                  'vendedor', 'qr_code', 'cantidad_items', 'items', 
                  'creado', 'actualizado']
        read_only_fields = ['id', 'numero', 'subtotal', 'total', 'cantidad_items', 
                           'qr_code', 'creado', 'actualizado']

class ItemVentaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear items de venta"""
    class Meta:
        model = ItemVenta
        fields = ['variante', 'cantidad', 'precio_unitario', 'descuento_item']
    
    def validate_variante(self, value):
        """Validar que la variante exista y tenga stock suficiente"""
        if not value.activo:
            raise serializers.ValidationError("La variante seleccionada no está activa")
        
        cantidad = self.initial_data.get('cantidad', 1)
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            raise serializers.ValidationError("La cantidad debe ser un número entero")
        
        if value.stock < cantidad:
            raise serializers.ValidationError(f"Stock insuficiente. Disponible: {value.stock}")
        
        return value
    
    def validate_cantidad(self, value):
        """Validar que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero")
        return value
    
    def validate_precio_unitario(self, value):
        """Validar que el precio unitario sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio unitario debe ser mayor que cero")
        return value

class VentaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear ventas"""
    items = ItemVentaCreateSerializer(many=True)
    
    class Meta:
        model = Venta
        fields = ['cliente', 'fecha', 'descuento', 'impuestos', 'estado', 
                  'metodo_pago', 'notas', 'vendedor', 'items']
    
    def validate_cliente(self, value):
        """Validar que el cliente exista y esté activo"""
        if not value.activo:
            raise serializers.ValidationError("El cliente seleccionado no está activo")
        return value
    
    def validate_items(self, value):
        """Validar que haya al menos un item en la venta"""
        if not value:
            raise serializers.ValidationError("Debe incluir al menos un item en la venta")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calcular subtotal inicial
        subtotal = 0
        for item_data in items_data:
            cantidad = item_data.get('cantidad', 1)
            precio = item_data.get('precio_unitario', 0)
            descuento = item_data.get('descuento_item', 0)
            subtotal += (cantidad * precio) - descuento
        
        # Crear venta
        venta = Venta.objects.create(
            subtotal=subtotal,
            total=subtotal - validated_data.get('descuento', 0) + validated_data.get('impuestos', 0),
            **validated_data
        )
        
        # Crear items y actualizar stock
        for item_data in items_data:
            variante = item_data['variante']
            cantidad = item_data['cantidad']
            
            # Actualizar stock
            variante.stock -= cantidad
            variante.save()
            
            # Crear item
            ItemVenta.objects.create(
                venta=venta,
                subtotal=(item_data['precio_unitario'] * cantidad) - item_data.get('descuento_item', 0),
                **item_data
            )
        
        return venta

class VentaUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar ventas"""
    class Meta:
        model = Venta
        fields = ['estado', 'metodo_pago', 'notas', 'vendedor']
    
    def validate_estado(self, value):
        """Validar cambios de estado"""
        # Si la venta ya está devuelta, no permitir cambios de estado
        if self.instance.estado == 'DEVUELTA' and value != 'DEVUELTA':
            raise serializers.ValidationError("No se puede cambiar el estado de una venta devuelta")
        return value

class ItemDevolucionSerializer(serializers.ModelSerializer):
    """Serializador para items de devolución"""
    item_venta_detalle = ItemVentaSerializer(source='item_venta', read_only=True)
    
    class Meta:
        model = ItemDevolucion
        fields = ['id', 'item_venta', 'item_venta_detalle', 'cantidad', 'monto']
        read_only_fields = ['id', 'item_venta_detalle']

class DevolucionSerializer(serializers.ModelSerializer):
    """Serializador para ver devoluciones"""
    items = ItemDevolucionSerializer(many=True, read_only=True)
    venta_numero = serializers.ReadOnlyField(source='venta.numero')
    motivo_display = serializers.ReadOnlyField(source='get_motivo_display')
    
    class Meta:
        model = Devolucion
        fields = ['id', 'venta', 'venta_numero', 'fecha', 'motivo', 'motivo_display', 
                  'descripcion', 'monto_devuelto', 'procesado_por', 'items']
        read_only_fields = ['id', 'venta_numero', 'motivo_display']

class ItemDevolucionCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear items de devolución"""
    class Meta:
        model = ItemDevolucion
        fields = ['item_venta', 'cantidad', 'monto']
    
    def validate_item_venta(self, value):
        """Validar que el item de venta pertenezca a la venta que se está devolviendo"""
        venta_id = self.context.get('venta_id')
        if value.venta.id != venta_id:
            raise serializers.ValidationError("El item no pertenece a la venta seleccionada")
        
        # Verificar si ya hay devoluciones para este item
        devoluciones_existentes = ItemDevolucion.objects.filter(item_venta=value)
        cantidad_devuelta = sum(d.cantidad for d in devoluciones_existentes)
        
        cantidad_disponible = value.cantidad - cantidad_devuelta
        if cantidad_disponible <= 0:
            raise serializers.ValidationError("Este item ya ha sido devuelto completamente")
        
        # Guardar la cantidad disponible para validar la cantidad a devolver
        self.context['cantidad_disponible'] = cantidad_disponible
        
        return value
    
    def validate_cantidad(self, value):
        """Validar que la cantidad a devolver sea válida"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero")
        
        cantidad_disponible = self.context.get('cantidad_disponible')
        if cantidad_disponible and value > cantidad_disponible:
            raise serializers.ValidationError(f"Solo puede devolver hasta {cantidad_disponible} unidades de este item")
        
        return value
    
    def validate_monto(self, value):
        """Validar que el monto sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor que cero")
        return value

class DevolucionCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear devoluciones"""
    items = ItemDevolucionCreateSerializer(many=True)
    
    class Meta:
        model = Devolucion
        fields = ['venta', 'fecha', 'motivo', 'descripcion', 'monto_devuelto', 'procesado_por', 'items']
    
    def validate_venta(self, value):
        """Validar que la venta exista y esté pagada"""
        if value.estado not in ['PAGADA', 'DEVUELTA']:
            raise serializers.ValidationError("Solo se pueden devolver ventas pagadas")
        return value
    
    def validate_items(self, value):
        """Validar que haya al menos un item en la devolución"""
        if not value:
            raise serializers.ValidationError("Debe incluir al menos un item en la devolución")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        venta = validated_data['venta']
        
        # Crear devolución
        devolucion = Devolucion.objects.create(**validated_data)
        
        # Crear items y actualizar stock
        for item_data in items_data:
            item_venta = item_data['item_venta']
            cantidad = item_data['cantidad']
            
            # Crear item de devolución
            ItemDevolucion.objects.create(
                devolucion=devolucion,
                **item_data
            )
        
        return devolucion