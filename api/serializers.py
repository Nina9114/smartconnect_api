from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Departamento, Sensor, Barrera, Evento


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario.
    Incluye validación de contraseña y campos de solo lectura.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text='Contraseña del usuario'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Confirmación de contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'rol', 'password', 'password_confirm', 'is_active',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        """Valida que las contraseñas coincidan."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Las contraseñas no coinciden.'
            })
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo usuario con contraseña encriptada."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Usuario.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Actualiza un usuario, manejando la contraseña por separado."""
        password_confirm = validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        if password:
            if password != password_confirm:
                raise serializers.ValidationError({
                    'password': 'Las contraseñas no coinciden.'
                })
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class UsuarioListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar usuarios (sin contraseña).
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
        read_only_fields = ['id']


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Departamento.
    """
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_nombre(self, value):
        """Valida que el nombre tenga al menos 3 caracteres."""
        if len(value) < 3:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 3 caracteres.'
            )
        return value


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Sensor.
    Incluye validación de UID único y estado válido.
    """
    departamento_nombre = serializers.CharField(
        source='departamento.nombre',
        read_only=True
    )
    usuario_username = serializers.CharField(
        source='usuario.username',
        read_only=True
    )
    
    class Meta:
        model = Sensor
        fields = [
            'id', 'uid', 'nombre', 'estado', 'departamento',
            'departamento_nombre', 'usuario', 'usuario_username',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_uid(self, value):
        """Valida que el UID sea único."""
        if self.instance and self.instance.uid == value:
            return value
        
        if Sensor.objects.filter(uid=value).exists():
            raise serializers.ValidationError(
                'Ya existe un sensor con este UID/MAC.'
            )
        return value
    
    def validate_nombre(self, value):
        """Valida que el nombre tenga al menos 3 caracteres."""
        if len(value) < 3:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 3 caracteres.'
            )
        return value


class BarreraSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Barrera.
    """
    departamento_nombre = serializers.CharField(
        source='departamento.nombre',
        read_only=True
    )
    
    class Meta:
        model = Barrera
        fields = [
            'id', 'nombre', 'estado', 'departamento',
            'departamento_nombre', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_actualizacion']


class EventoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Evento.
    Incluye información relacionada de sensor, departamento y usuario.
    """
    sensor_uid = serializers.CharField(
        source='sensor.uid',
        read_only=True
    )
    sensor_nombre = serializers.CharField(
        source='sensor.nombre',
        read_only=True
    )
    departamento_nombre = serializers.CharField(
        source='departamento.nombre',
        read_only=True
    )
    usuario_username = serializers.CharField(
        source='usuario.username',
        read_only=True
    )
    
    class Meta:
        model = Evento
        fields = [
            'id', 'tipo', 'resultado', 'sensor', 'sensor_uid',
            'sensor_nombre', 'departamento', 'departamento_nombre',
            'usuario', 'usuario_username', 'observaciones', 'fecha_evento'
        ]
        read_only_fields = ['id', 'fecha_evento']

