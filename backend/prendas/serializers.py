from rest_framework import serializers
from .models import Categoria, Talla, Color, Prenda, VariantePrenda, ImagenPrenda

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'slug', 'creado', 'actualizado']
        read_only_fields = ['slug', 'creado', 'actualizado']

class TallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = ['id', 'nombre', 'descripcion', 'orden']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'nombre', 'codigo_hex']

class ImagenPrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPrenda
        fields = ['id', 'imagen', 'titulo', 'orden', 'creado']
        read_only_fields = ['creado']

class VariantePrendaSerializer(serializers.ModelSerializer):
    talla_nombre = serializers.ReadOnlyField(source='talla.nombre')
    color_nombre = serializers.ReadOnlyField(source='color.nombre')
    color_hex = serializers.ReadOnlyField(source='color.codigo_hex')
    
    class Meta:
        model = VariantePrenda
        fields = ['id', 'talla', 'talla_nombre', 'color', 'color_nombre', 'color_hex', 
                  'stock', 'codigo_barras', 'imagen', 'activo', 'disponible', 
                  'creado', 'actualizado']
        read_only_fields = ['codigo_barras', 'disponible', 'creado', 'actualizado']

class VariantePrendaDetalleSerializer(VariantePrendaSerializer):
    talla = TallaSerializer(read_only=True)
    color = ColorSerializer(read_only=True)

class PrendaListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    stock_total = serializers.ReadOnlyField()
    tiene_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Prenda
        fields = ['id', 'codigo', 'nombre', 'categoria', 'categoria_nombre', 
                  'precio_venta', 'genero', 'imagen_principal', 'slug', 
                  'activo', 'stock_total', 'tiene_stock', 'creado']
        read_only_fields = ['codigo', 'slug', 'stock_total', 'tiene_stock', 'creado']

class PrendaDetalleSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    variantes = VariantePrendaSerializer(many=True, read_only=True)
    imagenes = ImagenPrendaSerializer(many=True, read_only=True)
    stock_total = serializers.ReadOnlyField()
    tiene_stock = serializers.ReadOnlyField()
    margen_ganancia = serializers.ReadOnlyField()
    
    class Meta:
        model = Prenda
        fields = ['id', 'codigo', 'nombre', 'descripcion', 'categoria', 
                  'precio_costo', 'precio_venta', 'genero', 'imagen_principal', 
                  'slug', 'activo', 'stock_total', 'tiene_stock', 'margen_ganancia',
                  'variantes', 'imagenes', 'creado', 'actualizado']
        read_only_fields = ['codigo', 'slug', 'stock_total', 'tiene_stock', 
                           'margen_ganancia', 'creado', 'actualizado']

class PrendaCreateUpdateSerializer(serializers.ModelSerializer):
    imagenes = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    class Meta:
        model = Prenda
        fields = ['nombre', 'descripcion', 'categoria', 'precio_costo',
                  'precio_venta', 'genero', 'imagen_principal', 'activo', 'imagenes']
    
    def validate(self, data):
        # Validar que el precio de venta sea mayor que el precio de costo
        if 'precio_venta' in data and 'precio_costo' in data:
            if data['precio_venta'] <= data['precio_costo']:
                raise serializers.ValidationError("El precio de venta debe ser mayor que el precio de costo")
        return data

    def create(self, validated_data):
        imagenes_data = validated_data.pop('imagenes', [])
        prenda = super().create(validated_data)

        # Crear una variante por defecto con stock 1
        try:
            default_talla = Talla.objects.first()
            default_color = Color.objects.first()
            if default_talla and default_color:
                VariantePrenda.objects.create(
                    prenda=prenda,
                    talla=default_talla,
                    color=default_color,
                    stock=1
                )
            else:
                print("Advertencia: No se pudo crear una variante por defecto. Asegúrese de que existan tallas y colores.")
        except Exception as e:
            print(f"Error al crear variante por defecto: {e}")

        # Crear imágenes adicionales
        for i, imagen_file in enumerate(imagenes_data):
            ImagenPrenda.objects.create(prenda=prenda, imagen=imagen_file, orden=i)

        return prenda

class ImagenPrendaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPrenda
        fields = ['prenda', 'imagen', 'titulo', 'orden']
        
    def validate_prenda(self, value):
        # Verificar que la prenda exista
        if not Prenda.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("La prenda especificada no existe")
        return value

class VariantePrendaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantePrenda
        fields = ['prenda', 'talla', 'color', 'stock', 'imagen', 'activo']
        
    def validate(self, data):
        # Verificar que no exista ya una variante con la misma combinación de prenda, talla y color
        if self.instance is None:  # Solo para creación
            if VariantePrenda.objects.filter(
                prenda=data['prenda'],
                talla=data['talla'],
                color=data['color']
            ).exists():
                raise serializers.ValidationError("Ya existe una variante con esta combinación de prenda, talla y color")
        return data