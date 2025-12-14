from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def handler404(request, exception):
    """
    Manejo personalizado de errores 404 para rutas no encontradas.
    Requerido por la evaluación.
    """
    return JsonResponse({
        'error': 'Ruta no encontrada',
        'detail': 'La ruta solicitada no existe',
        'status_code': 404
    }, status=404)


def handler500(request):
    """
    Manejo personalizado de errores 500.
    """
    return JsonResponse({
        'error': 'Error del servidor',
        'detail': 'Ha ocurrido un error interno',
        'status_code': 500
    }, status=500)

