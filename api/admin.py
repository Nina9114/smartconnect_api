from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Barrera, Evento


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Administración personalizada para el modelo Usuario."""
    list_display = ['username', 'email', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('rol',)}),
    )


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Administración para el modelo Departamento."""
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """Administración para el modelo Sensor."""
    list_display = ['nombre', 'uid', 'estado', 'departamento', 'usuario', 'fecha_creacion']
    list_filter = ['estado', 'departamento', 'fecha_creacion']
    search_fields = ['nombre', 'uid']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    """Administración para el modelo Barrera."""
    list_display = ['nombre', 'estado', 'departamento', 'fecha_actualizacion']
    list_filter = ['estado', 'departamento']
    search_fields = ['nombre']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Administración para el modelo Evento."""
    list_display = ['tipo', 'resultado', 'sensor', 'departamento', 'usuario', 'fecha_evento']
    list_filter = ['tipo', 'resultado', 'fecha_evento']
    search_fields = ['observaciones']
    readonly_fields = ['fecha_evento']
    date_hierarchy = 'fecha_evento'
