from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

Usuario = get_user_model()

class UsuarioListSerializer(serializers.ModelSerializer):
    """Serializador para listar usuarios"""
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'apellido', 'rol', 'is_active', 'ultimo_acceso']
        read_only_fields = ['id', 'ultimo_acceso']

class UsuarioDetailSerializer(serializers.ModelSerializer):
    """Serializador para detalles de usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'apellido', 'rol', 'telefono', 'foto', 
                  'is_active', 'is_staff', 'is_superuser', 'ultimo_acceso', 
                  'date_joined', 'creado', 'actualizado']
        read_only_fields = ['id', 'ultimo_acceso', 'date_joined', 'creado', 'actualizado']

class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear usuarios"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'rol', 'telefono', 'foto', 
                  'is_active', 'is_staff', 'password', 'password_confirm']
    
    def validate(self, attrs):
        # Validar que las contraseñas coincidan
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        # Validar la contraseña con las validaciones de Django
        try:
            validate_password(attrs.get('password'))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        # Validar que el email no exista
        if Usuario.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "Ya existe un usuario con este email."})
        
        return attrs
    
    def create(self, validated_data):
        # Eliminar password_confirm del diccionario
        validated_data.pop('password_confirm', None)
        
        # Crear el usuario
        password = validated_data.pop('password')
        user = Usuario.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar usuarios"""
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rol', 'telefono', 'foto', 'is_active', 'is_staff']

class CambiarPasswordSerializer(serializers.Serializer):
    """Serializador para cambiar la contraseña"""
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """Serializador para el perfil del usuario autenticado"""
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'apellido', 'rol', 'telefono', 'foto', 
                  'is_active', 'is_staff', 'is_superuser', 'ultimo_acceso']
        read_only_fields = ['id', 'email', 'rol', 'is_active', 'is_staff', 'is_superuser', 'ultimo_acceso']