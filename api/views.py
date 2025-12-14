from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Usuario, Departamento, Sensor, Barrera, Evento
from .serializers import (
    UsuarioSerializer, UsuarioListSerializer,
    DepartamentoSerializer,
    SensorSerializer,
    BarreraSerializer,
    EventoSerializer
)


class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado: Solo usuarios con rol 'admin' pueden acceder.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: Admin puede hacer todo, otros solo lectura.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'admin'
        )


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    Solo administradores pueden crear/editar/eliminar.
    """
    queryset = Usuario.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def registro(self, request):
        """
        Endpoint público para registro de usuarios.
        Por defecto crea usuarios con rol 'operador'.
        """
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UsuarioListSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Endpoint personalizado para login con JWT.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Se requiere username y password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Usuario inactivo'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UsuarioListSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar departamentos.
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly]


class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar sensores RFID.
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Sensor.objects.select_related('departamento', 'usuario').all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def intentar_acceso(self, request):
        """
        Endpoint para simular un intento de acceso con un sensor.
        Valida el sensor y crea un evento.
        """
        uid = request.data.get('uid')
        departamento_id = request.data.get('departamento_id')
        
        if not uid:
            return Response(
                {'error': 'Se requiere el UID del sensor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            sensor = Sensor.objects.get(uid=uid)
        except Sensor.DoesNotExist:
            # Crear evento de acceso denegado
            evento = Evento.objects.create(
                tipo='acceso_sensor',
                resultado='denegado',
                departamento_id=departamento_id,
                observaciones=f'Sensor con UID {uid} no encontrado'
            )
            return Response({
                'acceso': 'denegado',
                'motivo': 'Sensor no encontrado',
                'evento_id': evento.id
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar estado del sensor
        if sensor.estado != 'activo':
            evento = Evento.objects.create(
                tipo='acceso_sensor',
                resultado='denegado',
                sensor=sensor,
                departamento=sensor.departamento,
                observaciones=f'Sensor en estado: {sensor.get_estado_display()}'
            )
            return Response({
                'acceso': 'denegado',
                'motivo': f'Sensor en estado: {sensor.get_estado_display()}',
                'evento_id': evento.id
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Acceso permitido
        evento = Evento.objects.create(
            tipo='acceso_sensor',
            resultado='permitido',
            sensor=sensor,
            departamento=sensor.departamento,
            observaciones='Acceso exitoso'
        )
        
        return Response({
            'acceso': 'permitido',
            'sensor': SensorSerializer(sensor).data,
            'evento_id': evento.id
        }, status=status.HTTP_200_OK)


class BarreraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar barreras de acceso.
    Admin: CRUD completo
    Operador: Solo lectura
    """
    queryset = Barrera.objects.select_related('departamento').all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def abrir(self, request, pk=None):
        """
        Endpoint para abrir una barrera manualmente.
        """
        barrera = self.get_object()
        barrera.estado = 'abierta'
        barrera.save()
        
        # Crear evento
        Evento.objects.create(
            tipo='apertura_manual',
            resultado='permitido',
            departamento=barrera.departamento,
            usuario=request.user,
            observaciones=f'Barrera {barrera.nombre} abierta manualmente'
        )
        
        return Response({
            'mensaje': 'Barrera abierta',
            'barrera': BarreraSerializer(barrera).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cerrar(self, request, pk=None):
        """
        Endpoint para cerrar una barrera manualmente.
        """
        barrera = self.get_object()
        barrera.estado = 'cerrada'
        barrera.save()
        
        # Crear evento
        Evento.objects.create(
            tipo='cierre_manual',
            resultado='permitido',
            departamento=barrera.departamento,
            usuario=request.user,
            observaciones=f'Barrera {barrera.nombre} cerrada manualmente'
        )
        
        return Response({
            'mensaje': 'Barrera cerrada',
            'barrera': BarreraSerializer(barrera).data
        }, status=status.HTTP_200_OK)


class EventoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar eventos de acceso.
    Solo lectura para todos los usuarios autenticados.
    """
    queryset = Evento.objects.select_related(
        'sensor', 'departamento', 'usuario'
    ).all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]
