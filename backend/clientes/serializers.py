from rest_framework import serializers
from .models import Cliente, Contacto

class ClienteListSerializer(serializers.ModelSerializer):
    """Serializador para listar clientes con información básica"""
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'nombre_completo', 'telefono', 
                  'email', 'localidad', 'activo', 'fecha_registro']
        read_only_fields = ['id', 'nombre_completo', 'fecha_registro']

class ClienteDetailSerializer(serializers.ModelSerializer):
    """Serializador para ver detalles completos de un cliente"""
    total_compras = serializers.ReadOnlyField()
    monto_total_compras = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'nombre_completo', 'tipo_documento', 
                  'numero_documento', 'email', 'telefono', 'direccion', 'localidad', 
                  'provincia', 'codigo_postal', 'fecha_nacimiento', 'notas', 'activo', 
                  'fecha_registro', 'ultima_actualizacion', 'total_compras', 'monto_total_compras']
        read_only_fields = ['id', 'nombre_completo', 'fecha_registro', 
                           'ultima_actualizacion', 'total_compras', 'monto_total_compras']

class ClienteCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializador para crear y actualizar clientes"""
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'tipo_documento', 'numero_documento', 
                  'email', 'telefono', 'direccion', 'localidad', 'provincia', 
                  'codigo_postal', 'fecha_nacimiento', 'notas', 'activo']
        
    def validate_email(self, value):
        """Validar que el email sea único si se proporciona"""
        if value:
            # Verificar si existe otro cliente con el mismo email (excluyendo el cliente actual en caso de actualización)
            instance = getattr(self, 'instance', None)
            if instance:
                if Cliente.objects.filter(email=value).exclude(id=instance.id).exists():
                    raise serializers.ValidationError("Ya existe un cliente con este email")
            else:
                if Cliente.objects.filter(email=value).exists():
                    raise serializers.ValidationError("Ya existe un cliente con este email")
        return value
    
    def validate_numero_documento(self, value):
        """Validar que el número de documento sea único si se proporciona"""
        if value:
            # Verificar si existe otro cliente con el mismo número de documento (excluyendo el cliente actual en caso de actualización)
            instance = getattr(self, 'instance', None)
            if instance:
                if Cliente.objects.filter(numero_documento=value, tipo_documento=self.initial_data.get('tipo_documento', instance.tipo_documento)).exclude(id=instance.id).exists():
                    raise serializers.ValidationError("Ya existe un cliente con este número de documento")
            else:
                if Cliente.objects.filter(numero_documento=value, tipo_documento=self.initial_data.get('tipo_documento', 'DNI')).exists():
                    raise serializers.ValidationError("Ya existe un cliente con este número de documento")
        return value

class ContactoSerializer(serializers.ModelSerializer):
    """Serializador para contactos con clientes"""
    tipo_display = serializers.ReadOnlyField(source='get_tipo_display')
    
    class Meta:
        model = Contacto
        fields = ['id', 'cliente', 'tipo', 'tipo_display', 'fecha', 'asunto', 
                  'descripcion', 'realizado_por', 'seguimiento_requerido', 'fecha_seguimiento']
        read_only_fields = ['id', 'fecha', 'tipo_display']

class ContactoCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear contactos"""
    class Meta:
        model = Contacto
        fields = ['cliente', 'tipo', 'asunto', 'descripcion', 'realizado_por', 
                  'seguimiento_requerido', 'fecha_seguimiento']
        
    def validate_cliente(self, value):
        """Validar que el cliente exista y esté activo"""
        if not value.activo:
            raise serializers.ValidationError("No se puede registrar un contacto para un cliente inactivo")
        return value
    
    def validate(self, data):
        """Validar que si se requiere seguimiento, se proporcione una fecha"""
        if data.get('seguimiento_requerido', False) and not data.get('fecha_seguimiento'):
            raise serializers.ValidationError({"fecha_seguimiento": "Si se requiere seguimiento, debe proporcionar una fecha"})
        return data