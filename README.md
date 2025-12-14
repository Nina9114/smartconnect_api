# SmartConnect API

API RESTful desarrollada con Django Rest Framework para sistema de control de acceso inteligente con sensores RFID.

## 📋 Características

- ✅ Autenticación JWT
- ✅ CRUD completo para todas las entidades
- ✅ Permisos por roles (Admin/Operador)
- ✅ Validaciones de datos
- ✅ Manejo profesional de errores (400, 401, 403, 404, 500)
- ✅ Endpoint `/api/info/` con información del proyecto
- ✅ CORS configurado para desarrollo y producción

## 🚀 Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Aplicar migraciones

```bash
python manage.py migrate
```

### 3. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 4. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Endpoints de la API

### Información del Proyecto
- **GET** `/api/info/` - Información del proyecto (público)

### Autenticación
- **POST** `/api/usuarios/registro/` - Registro de nuevo usuario (público)
- **POST** `/api/usuarios/login/` - Login y obtención de token JWT (público)
- **POST** `/api/token/` - Obtener token JWT (público)
- **POST** `/api/token/refresh/` - Refrescar token JWT (público)

### Usuarios
- **GET** `/api/usuarios/` - Listar usuarios (requiere autenticación, solo Admin)
- **POST** `/api/usuarios/` - Crear usuario (requiere autenticación, solo Admin)
- **GET** `/api/usuarios/{id}/` - Detalle de usuario (requiere autenticación, solo Admin)
- **PUT/PATCH** `/api/usuarios/{id}/` - Actualizar usuario (requiere autenticación, solo Admin)
- **DELETE** `/api/usuarios/{id}/` - Eliminar usuario (requiere autenticación, solo Admin)

### Departamentos
- **GET** `/api/departamentos/` - Listar departamentos (requiere autenticación)
- **POST** `/api/departamentos/` - Crear departamento (requiere autenticación, solo Admin)
- **GET** `/api/departamentos/{id}/` - Detalle de departamento (requiere autenticación)
- **PUT/PATCH** `/api/departamentos/{id}/` - Actualizar departamento (requiere autenticación, solo Admin)
- **DELETE** `/api/departamentos/{id}/` - Eliminar departamento (requiere autenticación, solo Admin)

### Sensores
- **GET** `/api/sensores/` - Listar sensores (requiere autenticación)
- **POST** `/api/sensores/` - Crear sensor (requiere autenticación, solo Admin)
- **GET** `/api/sensores/{id}/` - Detalle de sensor (requiere autenticación)
- **PUT/PATCH** `/api/sensores/{id}/` - Actualizar sensor (requiere autenticación, solo Admin)
- **DELETE** `/api/sensores/{id}/` - Eliminar sensor (requiere autenticación, solo Admin)
- **POST** `/api/sensores/intentar_acceso/` - Simular intento de acceso con sensor (requiere autenticación)

### Barreras
- **GET** `/api/barreras/` - Listar barreras (requiere autenticación)
- **POST** `/api/barreras/` - Crear barrera (requiere autenticación, solo Admin)
- **GET** `/api/barreras/{id}/` - Detalle de barrera (requiere autenticación)
- **PUT/PATCH** `/api/barreras/{id}/` - Actualizar barrera (requiere autenticación, solo Admin)
- **DELETE** `/api/barreras/{id}/` - Eliminar barrera (requiere autenticación, solo Admin)
- **POST** `/api/barreras/{id}/abrir/` - Abrir barrera manualmente (requiere autenticación)
- **POST** `/api/barreras/{id}/cerrar/` - Cerrar barrera manualmente (requiere autenticación)

### Eventos
- **GET** `/api/eventos/` - Listar eventos (requiere autenticación, solo lectura)
- **GET** `/api/eventos/{id}/` - Detalle de evento (requiere autenticación, solo lectura)

## 🔐 Autenticación JWT

### Obtener Token

```bash
POST /api/token/
Content-Type: application/json

{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

Respuesta:
```json
{
  "access": "token_de_acceso",
  "refresh": "token_de_refresco"
}
```

### Usar Token en Requests

Incluir el token en el header `Authorization`:

```
Authorization: Bearer {token_de_acceso}
```

## 📝 Ejemplos de Uso

### Crear un Departamento

```bash
POST /api/departamentos/
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal",
  "activo": true
}
```

### Crear un Sensor

```bash
POST /api/sensores/
Authorization: Bearer {token}
Content-Type: application/json

{
  "uid": "ABC123XYZ",
  "nombre": "Tarjeta Juan Pérez",
  "estado": "activo",
  "departamento": 1
}
```

### Intentar Acceso con Sensor

```bash
POST /api/sensores/intentar_acceso/
Authorization: Bearer {token}
Content-Type: application/json

{
  "uid": "ABC123XYZ",
  "departamento_id": 1
}
```

## 🏗️ Modelos de Datos

- **Usuario**: Usuarios con roles (Admin/Operador)
- **Departamento**: Zonas o áreas físicas
- **Sensor**: Sensores RFID con UID único y estado
- **Barrera**: Control de barreras de acceso
- **Evento**: Registro de eventos de acceso

## 🔒 Permisos

- **Admin**: CRUD completo en todas las entidades
- **Operador**: Solo lectura en todas las entidades

## 📦 Estructura del Proyecto

```
smartconnect_api/
├── api/
│   ├── models.py          # Modelos de datos
│   ├── serializers.py     # Serializers de DRF
│   ├── views.py           # ViewSets y lógica de negocio
│   ├── urls.py            # URLs de la API
│   └── admin.py           # Configuración del admin
├── smartconnect/
│   ├── settings.py        # Configuración del proyecto
│   ├── urls.py            # URLs principales
│   ├── views.py           # Handlers de errores
│   └── exceptions.py      # Manejo de excepciones
├── manage.py
└── requirements.txt
```

## 🧪 Pruebas

Para probar la API puedes usar:
- **Postman**
- **Apidog**
- **curl**
- **httpie**

## 📄 Licencia

Este proyecto es parte de la evaluación de Programación Back End.

