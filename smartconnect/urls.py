"""
URL configuration for smartconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    Endpoint /api/info/ que devuelve información del proyecto.
    Requerido por la evaluación.
    """
    return Response({
        "autor": ["Magda"],  # Cambiar por tu nombre
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect API",
        "descripcion": "API RESTful para sistema de control de acceso inteligente con sensores RFID, gestión de usuarios, departamentos y eventos de acceso",
        "version": "1.0"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/info/', api_info, name='api-info'),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
