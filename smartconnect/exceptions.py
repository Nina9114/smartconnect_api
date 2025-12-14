from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied


def custom_exception_handler(exc, context):
    """
    Manejo personalizado de excepciones para la API.
    Proporciona respuestas JSON consistentes para todos los errores.
    """
    # Obtener la respuesta estándar de DRF
    response = exception_handler(exc, context)
    
    # Si no hay respuesta estándar, crear una personalizada
    if response is None:
        if isinstance(exc, Http404):
            response = Response(
                {
                    'error': 'Recurso no encontrado',
                    'detail': str(exc),
                    'status_code': 404
                },
                status=status.HTTP_404_NOT_FOUND
            )
        elif isinstance(exc, PermissionDenied):
            response = Response(
                {
                    'error': 'Permiso denegado',
                    'detail': 'No tiene permisos para realizar esta acción',
                    'status_code': 403
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            response = Response(
                {
                    'error': 'Error del servidor',
                    'detail': str(exc),
                    'status_code': 500
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        # Personalizar la respuesta de DRF
        custom_response_data = {
            'error': 'Error en la solicitud',
            'detail': response.data,
            'status_code': response.status_code
        }
        response.data = custom_response_data
    
    return response

