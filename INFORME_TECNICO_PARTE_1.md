# Informe Técnico - SmartConnect API
## Parte 1: Configuración Inicial y Estructura Base

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Comandos Utilizados](#comandos-utilizados)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Explicación Detallada de Archivos](#explicación-detallada-de-archivos)
5. [Flujo de Trabajo](#flujo-de-trabajo)
6. [Conceptos Clave Explicados](#conceptos-clave-explicados)

---

## Introducción

Este documento explica paso a paso cómo se creó la API RESTful **SmartConnect** desde cero. El proyecto utiliza Django y Django Rest Framework para crear un sistema de control de acceso inteligente con sensores RFID.

### ¿Qué es Django?
Django es un framework web de Python que facilita la creación de aplicaciones web complejas. Nos permite crear APIs (Application Programming Interfaces) que otras aplicaciones pueden consumir.

### ¿Qué es una API RESTful?
Una API RESTful es una forma de comunicar aplicaciones usando el protocolo HTTP. Permite que diferentes sistemas (aplicaciones móviles, IoT, otros servidores) se comuniquen entre sí usando métodos estándar como GET, POST, PUT, DELETE.

---

## Comandos Utilizados

### 1. Verificación de Python
```bash
python --version
```
**¿Por qué?** Necesitamos verificar que Python está instalado antes de comenzar. Django requiere Python 3.8 o superior.

**Resultado esperado:** `Python 3.13.9` (o similar)

---

### 2. Verificación de Django
```bash
python -m django --version
```
**¿Por qué?** Verificamos que Django está instalado y qué versión tenemos.

**Resultado esperado:** `5.2.7` (o similar)

---

### 3. Crear el Proyecto Django
```bash
python -m django startproject smartconnect .
```
**¿Por qué?** Este comando crea la estructura base del proyecto Django.

**Explicación detallada:**
- `python -m django`: Ejecuta Django como módulo de Python
- `startproject`: Comando que crea un nuevo proyecto
- `smartconnect`: Nombre del proyecto
- `.` (punto): Indica que el proyecto se creará en el directorio actual

**¿Qué crea este comando?**
- Carpeta `smartconnect/` con la configuración del proyecto
- Archivo `manage.py` para gestionar el proyecto
- Archivos de configuración iniciales

---

### 4. Crear la Aplicación API
```bash
python manage.py startapp api
```
**¿Por qué?** En Django, un proyecto puede tener múltiples aplicaciones. Creamos la app `api` que contendrá toda la lógica de nuestra API.

**Explicación detallada:**
- `manage.py`: Script de gestión de Django
- `startapp`: Comando para crear una nueva aplicación
- `api`: Nombre de nuestra aplicación

**¿Qué crea este comando?**
- Carpeta `api/` con la estructura básica de la aplicación
- Archivos: `models.py`, `views.py`, `admin.py`, `urls.py`, etc.

---

### 5. Instalar Dependencias
```bash
pip install -r requirements.txt
```
**¿Por qué?** Necesitamos instalar todas las librerías que nuestro proyecto requiere.

**Explicación detallada:**
- `pip`: Gestor de paquetes de Python
- `install`: Comando para instalar paquetes
- `-r requirements.txt`: Instala todos los paquetes listados en el archivo requirements.txt

**Paquetes instalados:**
- `Django==5.2.7`: Framework web principal
- `djangorestframework==3.15.2`: Extensión para crear APIs REST
- `djangorestframework-simplejwt==5.3.1`: Autenticación con tokens JWT
- `django-cors-headers==4.6.0`: Permite peticiones desde otros dominios
- `python-decouple==3.8`: Manejo seguro de variables de entorno

---

### 6. Crear Migraciones
```bash
python manage.py makemigrations
```
**¿Por qué?** Las migraciones son archivos que Django genera para crear/modificar las tablas en la base de datos según nuestros modelos.

**Explicación detallada:**
- `makemigrations`: Crea archivos de migración basados en los cambios en `models.py`
- Django compara los modelos actuales con el estado de la base de datos
- Genera archivos Python en `api/migrations/` que contienen las instrucciones SQL

**Resultado esperado:**
```
Migrations for 'api':
  api\migrations\0001_initial.py
    + Create model Departamento
    + Create model Usuario
    + Create model Barrera
    + Create model Sensor
    + Create model Evento
```

---

### 7. Aplicar Migraciones
```bash
python manage.py migrate
```
**¿Por qué?** Este comando ejecuta las migraciones y crea las tablas reales en la base de datos.

**Explicación detallada:**
- `migrate`: Ejecuta las migraciones pendientes
- Crea/modifica las tablas en la base de datos SQLite (por defecto)
- Aplica también las migraciones del sistema de Django (admin, auth, etc.)

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying api.0001_initial... OK
  ...
```

---

### 8. Verificar Configuración
```bash
python manage.py check
```
**¿Por qué?** Verifica que no haya errores de configuración antes de ejecutar el servidor.

**Explicación detallada:**
- Revisa la configuración del proyecto
- Verifica que las URLs estén bien configuradas
- Comprueba que no haya problemas con los modelos

**Resultado esperado:** `System check identified no issues (0 silenced).`

---

## Estructura del Proyecto

Después de ejecutar todos los comandos, la estructura del proyecto queda así:

```
smartconnect_api/
│
├── manage.py                    # Script principal de gestión de Django
├── db.sqlite3                   # Base de datos SQLite (se crea después de migrate)
├── requirements.txt             # Lista de dependencias del proyecto
├── README.md                    # Documentación del proyecto
├── .gitignore                   # Archivos a ignorar en Git
│
├── smartconnect/                # Carpeta de configuración del proyecto
│   ├── __init__.py             # Hace que Python trate esta carpeta como paquete
│   ├── settings.py             # ⭐ CONFIGURACIÓN PRINCIPAL DEL PROYECTO
│   ├── urls.py                 # ⭐ RUTAS PRINCIPALES DEL PROYECTO
│   ├── wsgi.py                 # Configuración para servidores WSGI
│   ├── asgi.py                 # Configuración para servidores ASGI
│   ├── views.py                # Handlers de errores personalizados
│   └── exceptions.py           # Manejo personalizado de excepciones
│
└── api/                         # Nuestra aplicación API
    ├── __init__.py             # Hace que Python trate esta carpeta como paquete
    ├── models.py               # ⭐ MODELOS DE DATOS (tablas de BD)
    ├── serializers.py          # ⭐ SERIALIZERS (conversión JSON ↔ Python)
    ├── views.py                # ⭐ LÓGICA DE NEGOCIO (endpoints)
    ├── urls.py                 # ⭐ RUTAS DE LA API
    ├── admin.py                # Configuración del panel de administración
    ├── apps.py                 # Configuración de la aplicación
    ├── tests.py                # Pruebas unitarias (vacío por ahora)
    └── migrations/              # Archivos de migración de base de datos
        └── 0001_initial.py     # Primera migración con todos los modelos
```

**⭐ = Archivos críticos que explicaremos en detalle**

---

## Explicación Detallada de Archivos

### 1. `requirements.txt`

**Ubicación:** Raíz del proyecto

**¿Qué es?** Lista todas las dependencias (librerías) que necesita el proyecto.

**Contenido:**
```txt
Django==5.2.7
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.6.0
python-decouple==3.8
```

**Explicación línea por línea:**
- `Django==5.2.7`: Framework web principal. El `==5.2.7` especifica la versión exacta.
- `djangorestframework==3.15.2`: Extensión que facilita crear APIs REST.
- `djangorestframework-simplejwt==5.3.1`: Librería para autenticación con tokens JWT.
- `django-cors-headers==4.6.0`: Permite que aplicaciones en otros dominios hagan peticiones a nuestra API.
- `python-decouple==3.8`: Facilita el manejo de variables de entorno de forma segura.

**¿Por qué es importante?** Permite que cualquier persona pueda instalar exactamente las mismas versiones de las librerías que usamos.

---

### 2. `smartconnect/settings.py`

**Ubicación:** `smartconnect/settings.py`

**¿Qué es?** Archivo de configuración central de Django. Aquí se configuran todas las características del proyecto.

#### Secciones Importantes:

##### A. `INSTALLED_APPS` (Líneas 33-46)
```python
INSTALLED_APPS = [
    'django.contrib.admin',           # Panel de administración
    'django.contrib.auth',           # Sistema de autenticación
    'django.contrib.contenttypes',    # Sistema de tipos de contenido
    'django.contrib.sessions',       # Manejo de sesiones
    'django.contrib.messages',       # Sistema de mensajes
    'django.contrib.staticfiles',    # Archivos estáticos (CSS, JS, imágenes)
    # Third party apps
    'rest_framework',                # Django Rest Framework
    'rest_framework_simplejwt',      # JWT para DRF
    'corsheaders',                   # CORS headers
    # Local apps
    'api',                           # Nuestra aplicación
]
```

**Explicación:**
- Django funciona con un sistema de "aplicaciones" instaladas.
- Cada aplicación añade funcionalidad al proyecto.
- `django.contrib.*` son aplicaciones incluidas con Django.
- `rest_framework` añade capacidades de API REST.
- `api` es nuestra aplicación personalizada.

##### B. `MIDDLEWARE` (Líneas 48-57)
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ⭐ IMPORTANTE: Debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**¿Qué es Middleware?** Son componentes que procesan las peticiones HTTP antes de que lleguen a nuestras vistas.

**Explicación línea por línea:**
- `SecurityMiddleware`: Añade headers de seguridad HTTP.
- `SessionMiddleware`: Maneja las sesiones de usuario.
- `CorsMiddleware`: **MUY IMPORTANTE** - Permite peticiones desde otros dominios. Debe ir antes de `CommonMiddleware`.
- `CommonMiddleware`: Procesa peticiones comunes.
- `CsrfViewMiddleware`: Protección contra ataques CSRF.
- `AuthenticationMiddleware`: Añade información del usuario autenticado.
- `MessagesMiddleware`: Maneja mensajes flash.
- `XFrameOptionsMiddleware`: Protección contra clickjacking.

##### C. `DATABASES` (Líneas 86-91)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Explicación:**
- Define qué base de datos usar.
- Por defecto usa SQLite (archivo local, perfecto para desarrollo).
- `BASE_DIR / 'db.sqlite3'` crea la ruta completa al archivo de base de datos.
- En producción, normalmente se usa PostgreSQL o MySQL.

##### D. `AUTH_USER_MODEL` (Línea 136)
```python
AUTH_USER_MODEL = 'api.Usuario'
```

**¿Por qué es importante?** Le dice a Django que use nuestro modelo personalizado `Usuario` en lugar del modelo de usuario por defecto.

**Explicación:**
- Django tiene un modelo de usuario por defecto.
- Creamos nuestro propio modelo `Usuario` con el campo `rol`.
- Esta línea le dice a Django que lo use.

##### E. `REST_FRAMEWORK` (Líneas 139-152)
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'smartconnect.exceptions.custom_exception_handler',
}
```

**Explicación detallada:**
- `DEFAULT_AUTHENTICATION_CLASSES`: Define que usaremos JWT para autenticación.
- `DEFAULT_PERMISSION_CLASSES`: Por defecto, todas las rutas requieren autenticación.
- `DEFAULT_PAGINATION_CLASS`: Divide las respuestas en páginas de 10 elementos.
- `DEFAULT_RENDERER_CLASSES`: Todas las respuestas serán en formato JSON.
- `EXCEPTION_HANDLER`: Usa nuestro manejo personalizado de errores.

##### F. `SIMPLE_JWT` (Líneas 157-162)
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # Token válido por 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # Refresh token válido por 1 día
    'ROTATE_REFRESH_TOKENS': True,                    # Rota el refresh token al usarlo
    'BLACKLIST_AFTER_ROTATION': True,                 # Invalida el token anterior
}
```

**Explicación:**
- Configura cuánto tiempo son válidos los tokens JWT.
- `ACCESS_TOKEN_LIFETIME`: El token de acceso expira en 1 hora.
- `REFRESH_TOKEN_LIFETIME`: El refresh token expira en 1 día.
- `ROTATE_REFRESH_TOKENS`: Cada vez que se refresca el token, se genera uno nuevo.
- `BLACKLIST_AFTER_ROTATION`: El token anterior se invalida (más seguro).

##### G. `CORS` (Líneas 165-170)
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React por defecto
    "http://localhost:8000",  # Django por defecto
]

CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo
```

**¿Qué es CORS?** Cross-Origin Resource Sharing. Permite que aplicaciones en otros dominios hagan peticiones a nuestra API.

**Explicación:**
- Por seguridad, los navegadores bloquean peticiones entre dominios diferentes.
- CORS permite especificar qué dominios pueden hacer peticiones.
- `CORS_ALLOW_ALL_ORIGINS = True` permite todos los dominios (solo para desarrollo).
- En producción, usar solo `CORS_ALLOWED_ORIGINS` con dominios específicos.

---

### 3. `api/models.py`

**Ubicación:** `api/models.py`

**¿Qué es?** Define la estructura de datos (tablas) de nuestra base de datos usando clases de Python.

**Concepto clave:** Los modelos son clases de Python que Django convierte automáticamente en tablas de base de datos.

#### Modelo 1: `Usuario` (Líneas 6-29)

```python
class Usuario(AbstractUser):
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
```

**Explicación detallada:**
- `class Usuario(AbstractUser)`: Hereda de `AbstractUser`, que incluye campos como `username`, `email`, `password`, etc.
- `ROL_CHOICES`: Lista de opciones para el campo `rol`. Cada tupla tiene `(valor_en_bd, texto_mostrado)`.
- `rol = models.CharField(...)`: Campo de texto con máximo 20 caracteres.
- `choices=ROL_CHOICES`: Limita los valores posibles a los definidos en `ROL_CHOICES`.
- `default='operador'`: Valor por defecto si no se especifica.

**¿Qué campos hereda de AbstractUser?**
- `username`: Nombre de usuario (único)
- `email`: Correo electrónico
- `password`: Contraseña (encriptada)
- `first_name`, `last_name`: Nombres
- `is_active`: Si el usuario está activo
- `date_joined`: Fecha de registro
- Y muchos más...

#### Modelo 2: `Departamento` (Líneas 32-58)

```python
class Departamento(models.Model):
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
```

**Explicación detallada:**
- `nombre`: Campo de texto con máximo 100 caracteres.
- `validators=[MinLengthValidator(3)]`: Valida que tenga al menos 3 caracteres.
- `descripcion`: Campo de texto largo. `blank=True` permite que esté vacío en formularios, `null=True` permite NULL en BD.
- `activo`: Campo booleano (True/False), por defecto True.
- `fecha_creacion`: Se llena automáticamente al crear (`auto_now_add=True`).
- `fecha_actualizacion`: Se actualiza automáticamente cada vez que se modifica (`auto_now=True`).

**Clase Meta:**
```python
class Meta:
    verbose_name = 'Departamento'
    verbose_name_plural = 'Departamentos'
    db_table = 'departamentos'
    ordering = ['nombre']
```

- `verbose_name`: Nombre singular para el admin.
- `verbose_name_plural`: Nombre plural para el admin.
- `db_table`: Nombre de la tabla en la base de datos.
- `ordering`: Orden por defecto al consultar (por nombre ascendente).

#### Modelo 3: `Sensor` (Líneas 61-115)

```python
class Sensor(models.Model):
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
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
```

**Explicación detallada:**
- `uid`: Código único del sensor. `unique=True` garantiza que no haya duplicados.
- `departamento = models.ForeignKey(...)`: **Relación muchos-a-uno**. Muchos sensores pueden pertenecer a un departamento.
  - `on_delete=models.SET_NULL`: Si se elimina el departamento, el sensor queda con `departamento=None`.
  - `related_name='sensores'`: Permite acceder a los sensores desde un departamento: `departamento.sensores.all()`.
- `usuario = models.ForeignKey(...)`: Relación muchos-a-uno con Usuario.

**Tipos de relaciones:**
- `ForeignKey`: Muchos-a-uno (muchos sensores → un departamento)
- `ManyToManyField`: Muchos-a-muchos
- `OneToOneField`: Uno-a-uno

#### Modelo 4: `Barrera` (Líneas 118-153)

Similar a los anteriores, pero con relación obligatoria a Departamento:
```python
departamento = models.ForeignKey(
    Departamento,
    on_delete=models.CASCADE,  # ⚠️ Si se elimina el departamento, se elimina la barrera
    related_name='barreras',
)
```

**Diferencia importante:** `on_delete=models.CASCADE` elimina la barrera si se elimina el departamento (relación más fuerte).

#### Modelo 5: `Evento` (Líneas 156-219)

```python
class Evento(models.Model):
    tipo = models.CharField(choices=TIPO_CHOICES, ...)
    resultado = models.CharField(choices=RESULTADO_CHOICES, ...)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, ...)
    departamento = models.ForeignKey(Departamento, ...)
    usuario = models.ForeignKey(Usuario, ...)
    fecha_evento = models.DateTimeField(auto_now_add=True)
```

**Explicación:**
- Registra todos los eventos de acceso.
- Puede tener sensor (si fue acceso con RFID) o no (si fue manual).
- Relaciona sensor, departamento y usuario.

---

### 4. `api/serializers.py`

**Ubicación:** `api/serializers.py`

**¿Qué es?** Los serializers convierten objetos Python (modelos) a JSON y viceversa. También validan los datos.

**Concepto clave:** 
- **Serialización**: Python → JSON (para enviar datos)
- **Deserialización**: JSON → Python (para recibir datos)

#### Serializer 1: `UsuarioSerializer` (Líneas 6-69)

```python
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Solo se usa al escribir, no se muestra al leer
        required=True,
        validators=[validate_password],  # Valida que la contraseña sea segura
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
```

**Explicación detallada:**
- `ModelSerializer`: Serializer automático basado en el modelo.
- `write_only=True`: El campo solo se usa al crear/actualizar, no aparece en las respuestas (por seguridad).
- `validators=[validate_password]`: Valida que la contraseña cumpla requisitos de seguridad.

**Método `validate` (Líneas 36-42):**
```python
def validate(self, attrs):
    if attrs['password'] != attrs['password_confirm']:
        raise serializers.ValidationError({
            'password': 'Las contraseñas no coinciden.'
        })
    return attrs
```

**¿Qué hace?** Valida que las contraseñas coincidan antes de guardar.

**Método `create` (Líneas 44-51):**
```python
def create(self, validated_data):
    validated_data.pop('password_confirm')  # Elimina el campo de confirmación
    password = validated_data.pop('password')  # Extrae la contraseña
    user = Usuario.objects.create(**validated_data)  # Crea el usuario
    user.set_password(password)  # ⭐ Encripta la contraseña
    user.save()
    return user
```

**¿Por qué `set_password`?** Las contraseñas NUNCA se guardan en texto plano. `set_password` las encripta usando un hash seguro.

#### Serializer 2: `SensorSerializer` (Líneas 100-140)

```python
def validate_uid(self, value):
    if self.instance and self.instance.uid == value:
        return value  # Si es la misma instancia, no validar
    
    if Sensor.objects.filter(uid=value).exists():
        raise serializers.ValidationError(
            'Ya existe un sensor con este UID/MAC.'
        )
    return value
```

**Explicación:** Valida que el UID sea único. Si estamos actualizando (`self.instance` existe) y el UID no cambió, no valida.

**Campos calculados:**
```python
departamento_nombre = serializers.CharField(
    source='departamento.nombre',
    read_only=True
)
```

**¿Qué hace?** Incluye el nombre del departamento en la respuesta JSON sin necesidad de hacer otra consulta.

---

### 5. `api/views.py`

**Ubicación:** `api/views.py`

**¿Qué es?** Contiene la lógica de negocio y define los endpoints de la API.

#### Clases de Permisos (Líneas 20-43)

```python
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'admin'
        )
```

**Explicación:**
- Clase personalizada que verifica si el usuario es admin.
- `request.user`: Usuario actual (obtenido del token JWT).
- `is_authenticated`: Verifica que esté autenticado.
- `rol == 'admin'`: Verifica que tenga rol de administrador.

```python
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user and request.user.is_authenticated
        return request.user.rol == 'admin'  # POST, PUT, DELETE solo para admin
```

**Explicación:**
- Métodos seguros (GET): Cualquier usuario autenticado puede leer.
- Métodos de escritura (POST, PUT, DELETE): Solo admin.

#### ViewSet: `UsuarioViewSet` (Líneas 46-109)

```python
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [IsAdmin]
```

**¿Qué es ModelViewSet?** Proporciona automáticamente:
- `list()` → GET `/api/usuarios/`
- `create()` → POST `/api/usuarios/`
- `retrieve()` → GET `/api/usuarios/{id}/`
- `update()` → PUT `/api/usuarios/{id}/`
- `partial_update()` → PATCH `/api/usuarios/{id}/`
- `destroy()` → DELETE `/api/usuarios/{id}/`

**Acción personalizada `login` (Líneas 76-109):**
```python
@action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
def login(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UsuarioListSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
```

**Explicación paso a paso:**
1. `@action`: Decorador que crea un endpoint personalizado.
2. `detail=False`: No requiere un ID específico (no es `/api/usuarios/{id}/login`).
3. `methods=['post']`: Solo acepta peticiones POST.
4. `permission_classes=[permissions.AllowAny]`: Cualquiera puede acceder (público).
5. `authenticate()`: Verifica las credenciales.
6. `RefreshToken.for_user()`: Genera tokens JWT para el usuario.
7. Retorna el usuario y los tokens.

#### ViewSet: `SensorViewSet` - Acción `intentar_acceso` (Líneas 133-192)

```python
@action(detail=False, methods=['post'])
def intentar_acceso(self, request):
    uid = request.data.get('uid')
    
    try:
        sensor = Sensor.objects.get(uid=uid)
    except Sensor.DoesNotExist:
        # Crear evento de acceso denegado
        evento = Evento.objects.create(...)
        return Response({'acceso': 'denegado', ...}, status=404)
    
    if sensor.estado != 'activo':
        # Crear evento de acceso denegado
        return Response({'acceso': 'denegado', ...}, status=403)
    
    # Acceso permitido
    evento = Evento.objects.create(
        tipo='acceso_sensor',
        resultado='permitido',
        sensor=sensor,
        departamento=sensor.departamento,
    )
    return Response({'acceso': 'permitido', ...}, status=200)
```

**Explicación:**
- Simula un intento de acceso con un sensor RFID.
- Busca el sensor por UID.
- Valida que el sensor exista y esté activo.
- Crea un evento registrando el intento.
- Retorna el resultado (permitido/denegado).

---

### 6. `smartconnect/urls.py`

**Ubicación:** `smartconnect/urls.py`

**¿Qué es?** Archivo principal de rutas. Define qué URL llama a qué vista.

```python
urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administración Django
    path('api/info/', api_info, name='api-info'),  # Endpoint de información
    path('api/', include('api.urls')),  # Incluye todas las rutas de la app api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**Explicación línea por línea:**
- `path('admin/', ...)`: Panel de administración en `/admin/`.
- `path('api/info/', ...)`: Endpoint personalizado que retorna información del proyecto.
- `path('api/', include('api.urls'))`: Incluye todas las rutas definidas en `api/urls.py`.
- `path('api/token/', ...)`: Endpoint para obtener token JWT.
- `path('api/token/refresh/', ...)`: Endpoint para refrescar token JWT.

**Función `api_info` (Líneas 24-37):**
```python
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    return Response({
        "autor": ["Magda"],
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect API",
        "descripcion": "...",
        "version": "1.0"
    })
```

**Explicación:**
- `@api_view(['GET'])`: Decorador que indica que es una vista de API que acepta GET.
- `@permission_classes([AllowAny])`: Cualquiera puede acceder (público).
- Retorna JSON con información del proyecto.

---

### 7. `api/urls.py`

**Ubicación:** `api/urls.py`

**¿Qué es?** Define las rutas específicas de nuestra aplicación API usando routers de DRF.

```python
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'barreras', BarreraViewSet, basename='barrera')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    path('', include(router.urls)),
]
```

**Explicación:**
- `DefaultRouter()`: Router que crea automáticamente rutas RESTful.
- `router.register(...)`: Registra un ViewSet y crea automáticamente:
  - `GET /api/usuarios/` → Lista usuarios
  - `POST /api/usuarios/` → Crea usuario
  - `GET /api/usuarios/{id}/` → Detalle de usuario
  - `PUT /api/usuarios/{id}/` → Actualiza usuario
  - `DELETE /api/usuarios/{id}/` → Elimina usuario
  - Y acciones personalizadas como `/api/usuarios/login/`

**¿Por qué usar routers?** Evita escribir manualmente cada ruta. El router las genera automáticamente.

---

### 8. `api/admin.py`

**Ubicación:** `api/admin.py`

**¿Qué es?** Configura cómo se muestran los modelos en el panel de administración de Django.

```python
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active', 'is_staff']
```

**Explicación:**
- `@admin.register(Usuario)`: Registra el modelo en el admin.
- `list_display`: Columnas que se muestran en la lista.
- `list_filter`: Filtros laterales para buscar fácilmente.

**¿Para qué sirve?** Permite gestionar los datos desde una interfaz web sin escribir código.

---

### 9. `smartconnect/views.py`

**Ubicación:** `smartconnect/views.py`

**¿Qué es?** Handlers personalizados para errores HTTP.

```python
def handler404(request, exception):
    return JsonResponse({
        'error': 'Ruta no encontrada',
        'detail': 'La ruta solicitada no existe',
        'status_code': 404
    }, status=404)
```

**Explicación:**
- Se ejecuta cuando alguien accede a una URL que no existe.
- Retorna JSON en lugar de HTML (importante para API).
- Requerido por la evaluación.

---

### 10. `smartconnect/exceptions.py`

**Ubicación:** `smartconnect/exceptions.py`

**¿Qué es?** Manejo personalizado de excepciones para respuestas JSON consistentes.

```python
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        # Manejar errores no manejados por DRF
        response = Response({
            'error': 'Error del servidor',
            'detail': str(exc),
            'status_code': 500
        }, status=500)
    else:
        # Personalizar respuesta de DRF
        custom_response_data = {
            'error': 'Error en la solicitud',
            'detail': response.data,
            'status_code': response.status_code
        }
        response.data = custom_response_data
    
    return response
```

**Explicación:**
- Intercepta todas las excepciones.
- Convierte errores a formato JSON consistente.
- Asegura que todos los errores tengan el mismo formato.

---

## Flujo de Trabajo

### 1. Petición HTTP llega al servidor

```
Cliente (Postman/Apidog) 
    ↓
    HTTP Request: GET /api/departamentos/
    ↓
Servidor Django
```

### 2. Django procesa la petición

```
1. Middleware procesa la petición:
   - SecurityMiddleware → Añade headers de seguridad
   - CorsMiddleware → Verifica CORS
   - AuthenticationMiddleware → Extrae token JWT y obtiene usuario
   
2. Django busca la ruta en urls.py:
   - smartconnect/urls.py → Encuentra path('api/', include('api.urls'))
   - api/urls.py → Router encuentra 'departamentos' → DepartamentoViewSet
   
3. ViewSet procesa la petición:
   - Verifica permisos (IsAdminOrReadOnly)
   - Si es GET → ejecuta list()
   - Obtiene datos: Departamento.objects.all()
   - Serializa: DepartamentoSerializer(queryset, many=True)
   - Retorna JSON
```

### 3. Respuesta al cliente

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Recepción",
      "descripcion": "Área de recepción",
      "activo": true,
      "fecha_creacion": "2024-01-15T10:30:00Z",
      "fecha_actualizacion": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Conceptos Clave Explicados

### ¿Qué es un Modelo?
Un modelo es una clase de Python que representa una tabla en la base de datos. Django convierte automáticamente los modelos en tablas SQL.

**Ejemplo:**
```python
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
```

Se convierte en:
```sql
CREATE TABLE departamentos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
```

### ¿Qué es un Serializer?
Un serializer convierte objetos Python a JSON (y viceversa). También valida los datos.

**Ejemplo:**
```python
# Python → JSON
departamento = Departamento.objects.get(id=1)
serializer = DepartamentoSerializer(departamento)
json_data = serializer.data
# Resultado: {"id": 1, "nombre": "Recepción", ...}

# JSON → Python
json_data = {"nombre": "Nuevo Departamento"}
serializer = DepartamentoSerializer(data=json_data)
if serializer.is_valid():
    departamento = serializer.save()  # Crea en BD
```

### ¿Qué es un ViewSet?
Un ViewSet es una clase que agrupa la lógica para manejar operaciones CRUD (Create, Read, Update, Delete) de un modelo.

**Ventajas:**
- Código más limpio y organizado
- Genera automáticamente múltiples endpoints
- Facilita el mantenimiento

### ¿Qué es JWT?
JWT (JSON Web Token) es un estándar para autenticación sin sesiones.

**Cómo funciona:**
1. Usuario hace login con username/password
2. Servidor valida credenciales
3. Servidor genera un token JWT
4. Cliente guarda el token
5. Cliente envía el token en cada petición: `Authorization: Bearer {token}`
6. Servidor valida el token y obtiene el usuario

**Ventajas:**
- No requiere sesiones en el servidor
- Escalable (funciona con múltiples servidores)
- Estándar de la industria

### ¿Qué es CORS?
CORS permite que aplicaciones web en un dominio accedan a recursos en otro dominio.

**Ejemplo:**
- Frontend en: `http://localhost:3000`
- API en: `http://localhost:8000`
- Sin CORS: ❌ Bloqueado por el navegador
- Con CORS: ✅ Permitido

### ¿Qué son las Migraciones?
Las migraciones son archivos que Django genera para modificar la estructura de la base de datos.

**Proceso:**
1. Modificas `models.py`
2. Ejecutas `makemigrations` → Genera archivos de migración
3. Ejecutas `migrate` → Aplica cambios a la BD

**Ventajas:**
- Versionado de la estructura de BD
- Puedes revertir cambios
- Facilita el trabajo en equipo

---

## Resumen de lo Implementado

### ✅ Completado en esta Parte:

1. **Proyecto Django creado** con estructura base
2. **Aplicación `api` creada** con todos los archivos necesarios
3. **5 Modelos implementados:**
   - Usuario (con roles)
   - Departamento
   - Sensor (RFID)
   - Barrera
   - Evento
4. **Serializers creados** con validaciones
5. **ViewSets implementados** con CRUD completo
6. **Autenticación JWT configurada**
7. **Sistema de permisos** (Admin/Operador)
8. **Manejo de errores personalizado**
9. **Endpoint `/api/info/` creado**
10. **CORS configurado** para desarrollo

### 📊 Estadísticas:

- **Archivos creados:** ~15 archivos principales
- **Modelos:** 5 modelos con relaciones
- **Serializers:** 6 serializers
- **ViewSets:** 5 ViewSets con acciones personalizadas
- **Endpoints:** ~30+ endpoints automáticos + personalizados
- **Líneas de código:** ~1000+ líneas

---

## Próximos Pasos

1. **Probar el servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Probar endpoints** con Postman/Apidog

4. **Preparar para AWS:**
   - Configurar variables de entorno
   - Cambiar base de datos a PostgreSQL
   - Configurar `ALLOWED_HOSTS`

---

## Conclusión

En esta primera parte, hemos establecido la base sólida de la API SmartConnect. Hemos creado:
- La estructura del proyecto
- Los modelos de datos con sus relaciones
- Los serializers con validaciones
- Los ViewSets con lógica de negocio
- La autenticación y permisos
- El manejo de errores

El proyecto está listo para ser probado localmente y posteriormente desplegado en AWS.

---

**Autor:** Magda  
**Fecha:** 2024  
**Versión:** 1.0

