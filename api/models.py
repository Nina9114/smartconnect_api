from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class Usuario(AbstractUser):
    """
    Modelo de Usuario extendido con roles.
    Hereda de AbstractUser para tener todos los campos básicos de Django.
    """
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='operador',
        help_text='Rol del usuario en el sistema'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


class Departamento(models.Model):
    """
    Modelo que representa un departamento o zona física.
    Un sensor pertenece a un departamento.
    """
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        help_text='Nombre del departamento o zona'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción del departamento'
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        db_table = 'departamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Sensor(models.Model):
    """
    Modelo que representa un sensor RFID (tarjeta o llavero).
    Debe tener un código único (UID/MAC) y un estado.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido'),
    ]
    
    uid = models.CharField(
        max_length=50,
        unique=True,
        help_text='Código único del sensor RFID (UID/MAC)'
    )
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        help_text='Nombre descriptivo del sensor'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='inactivo',
        help_text='Estado actual del sensor'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        help_text='Departamento al que pertenece el sensor'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        help_text='Usuario al que está vinculado el sensor'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        db_table = 'sensores'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.uid})"


class Barrera(models.Model):
    """
    Modelo que representa el estado de la barrera de acceso.
    Control manual desde API.
    """
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        default='Barrera Principal',
        help_text='Nombre de la barrera'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='cerrada',
        help_text='Estado actual de la barrera'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='barreras',
        help_text='Departamento donde se encuentra la barrera'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Barrera'
        verbose_name_plural = 'Barreras'
        db_table = 'barreras'
    
    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"


class Evento(models.Model):
    """
    Modelo que registra eventos de acceso.
    Puede ser un intento de acceso con sensor o una acción manual.
    """
    TIPO_CHOICES = [
        ('acceso_sensor', 'Acceso con Sensor'),
        ('apertura_manual', 'Apertura Manual'),
        ('cierre_manual', 'Cierre Manual'),
    ]
    
    RESULTADO_CHOICES = [
        ('permitido', 'Permitido'),
        ('denegado', 'Denegado'),
    ]
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        help_text='Tipo de evento'
    )
    resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        help_text='Resultado del evento'
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos',
        help_text='Sensor que generó el evento (si aplica)'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        related_name='eventos',
        help_text='Departamento donde ocurrió el evento'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos',
        help_text='Usuario que generó el evento (si fue manual)'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text='Observaciones adicionales del evento'
    )
    fecha_evento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        db_table = 'eventos'
        ordering = ['-fecha_evento']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.get_resultado_display()} ({self.fecha_evento})"
