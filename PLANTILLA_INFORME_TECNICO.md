# Informe Técnico - SmartConnect API
## Evaluación Sumativa IV - Programación Back End

**Estudiante:** [Tu Nombre Completo]  
**RUT:** [Tu RUT]  
**Asignatura:** Programación Back End  
**Código:** TI3041  
**Fecha:** [Fecha de Entrega]

---

## 📋 Tabla de Contenidos

1. [Arquitectura General](#1-arquitectura-general)
2. [Modelos y Relaciones](#2-modelos-y-relaciones)
3. [Endpoints de la API](#3-endpoints-de-la-api)
4. [Pruebas en AWS](#4-pruebas-en-aws)
5. [Autenticación JWT](#5-autenticación-jwt)
6. [Manejo de Errores](#6-manejo-de-errores)
7. [Capturas de Pruebas](#7-capturas-de-pruebas)

---

## 1. Arquitectura General

### 1.1 Descripción del Proyecto

SmartConnect es una API RESTful desarrollada con Django Rest Framework para gestionar un sistema de control de acceso inteligente con sensores RFID. La API permite administrar usuarios, departamentos, sensores, barreras y eventos de acceso.

### 1.2 Estructura del Proyecto

```
smartconnect_api/
├── api/                    # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── serializers.py     # Serializers para JSON
│   ├── views.py           # ViewSets y lógica de negocio
│   ├── urls.py            # Rutas de la API
│   └── admin.py           # Configuración del admin
├── smartconnect/          # Configuración del proyecto
│   ├── settings.py       # Configuración (DB, JWT, CORS)
│   ├── urls.py           # URLs principales
│   ├── views.py          # Handlers de errores
│   └── exceptions.py     # Manejo de excepciones
├── requirements.txt      # Dependencias
└── manage.py            # Script de gestión Django
```

### 1.3 Tecnologías Utilizadas

- **Backend:** Django 5.2.7
- **API:** Django Rest Framework 3.15.2
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Base de Datos:** MySQL (producción) / SQLite (desarrollo)
- **Servidor WSGI:** Gunicorn
- **Despliegue:** AWS EC2

### 1.4 Flujo de Peticiones

```
Cliente (Postman) 
    ↓ HTTP Request
Servidor Django (EC2)
    ↓ Middleware (CORS, Auth, etc.)
ViewSet (api/views.py)
    ↓ Serializer (validación)
Modelo (api/models.py)
    ↓ Base de Datos MySQL
Respuesta JSON
    ↓ HTTP Response
Cliente
```

---

## 2. Modelos y Relaciones

### 2.1 Modelo Lógico

```
┌─────────────┐
│   Usuario   │
│─────────────│
│ id (PK)     │
│ username    │◄────┐
│ email       │     │
│ password    │     │
│ rol         │     │
└─────────────┘     │
                     │
┌─────────────┐     │
│ Departamento│     │
│─────────────│     │
│ id (PK)     │     │
│ nombre      │     │
│ descripcion │     │
│ activo      │     │
└─────────────┘     │
      │              │
      │ 1            │ N
      │              │
      │ N            │
┌─────────────┐     │
│   Sensor    │─────┘
│─────────────│
│ id (PK)     │
│ uid (UK)    │
│ nombre      │
│ estado      │
│ departamento│─────┐
│ usuario     │     │
└─────────────┘     │
      │              │
      │ 1            │ N
      │              │
┌─────────────┐     │
│   Evento    │─────┘
│─────────────│
│ id (PK)     │
│ tipo        │
│ resultado   │
│ sensor      │
│ departamento│
│ usuario     │
│ fecha_evento│
└─────────────┘

┌─────────────┐
│   Barrera   │
│─────────────│
│ id (PK)     │
│ nombre      │
│ estado      │
│ departamento│─────┐
└─────────────┘     │
                     │
              ┌──────┘
              │ N
      ┌───────┴───────┐
      │  Departamento │
      └───────────────┘
```

### 2.2 Descripción de Modelos

#### Usuario
- **Propósito:** Gestionar usuarios del sistema con roles
- **Campos principales:** username, email, password, rol (admin/operador)
- **Relaciones:** 
  - 1:N con Sensor (un usuario puede tener múltiples sensores)
  - 1:N con Evento (un usuario puede generar múltiples eventos)

#### Departamento
- **Propósito:** Representar zonas o áreas físicas
- **Campos principales:** nombre, descripcion, activo
- **Relaciones:**
  - 1:N con Sensor (un departamento puede tener múltiples sensores)
  - 1:N con Barrera (un departamento puede tener múltiples barreras)
  - 1:N con Evento (un departamento puede tener múltiples eventos)

#### Sensor
- **Propósito:** Representar sensores RFID (tarjetas o llaveros)
- **Campos principales:** uid (único), nombre, estado (activo/inactivo/bloqueado/perdido)
- **Relaciones:**
  - N:1 con Departamento
  - N:1 con Usuario
  - 1:N con Evento

#### Barrera
- **Propósito:** Controlar el estado de barreras de acceso
- **Campos principales:** nombre, estado (abierta/cerrada)
- **Relaciones:**
  - N:1 con Departamento

#### Evento
- **Propósito:** Registrar todos los eventos de acceso
- **Campos principales:** tipo, resultado (permitido/denegado), fecha_evento
- **Relaciones:**
  - N:1 con Sensor (opcional)
  - N:1 con Departamento
  - N:1 con Usuario (opcional)

---

## 3. Endpoints de la API

### 3.1 Endpoints Públicos (Sin Autenticación)

#### GET /api/info/
- **Método:** GET
- **Descripción:** Retorna información del proyecto
- **Autenticación:** No requiere token JWT
- **Códigos HTTP:** 200 OK
- **Ejemplo de Respuesta:**
```json
{
  "autor": ["Magda"],
  "asignatura": "Programación Back End",
  "proyecto": "SmartConnect API",
  "descripcion": "API RESTful para sistema de control de acceso inteligente",
  "version": "1.0"
}
```

#### POST /api/usuarios/login/
- **Método:** POST
- **Descripción:** Autenticación de usuario y obtención de tokens JWT
- **Autenticación:** No requiere token JWT
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized
- **Ejemplo de Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```
- **Ejemplo de Respuesta (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "rol": "admin",
    "is_active": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/token/
- **Método:** POST
- **Descripción:** Endpoint estándar de JWT para obtener tokens
- **Autenticación:** No requiere token JWT
- **Códigos HTTP:** 200 OK, 401 Unauthorized
- **Ejemplo de Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

#### POST /api/token/refresh/
- **Método:** POST
- **Descripción:** Renovar access token usando refresh token
- **Autenticación:** No requiere token JWT
- **Códigos HTTP:** 200 OK, 401 Unauthorized
- **Ejemplo de Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
- **Ejemplo de Respuesta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/usuarios/registro/
- **Método:** POST
- **Descripción:** Registro público de nuevos usuarios (crea usuarios con rol 'operador' por defecto)
- **Autenticación:** No requiere token JWT
- **Códigos HTTP:** 201 Created, 400 Bad Request
- **Ejemplo de Request:**
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "operador"
}
```
- **Ejemplo de Respuesta (201 Created):**
```json
{
  "user": {
    "id": 2,
    "username": "nuevo_usuario",
    "email": "usuario@example.com",
    "rol": "operador",
    "is_active": true
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3.2 Endpoints de Departamentos

#### GET /api/departamentos/
- **Método:** GET
- **Descripción:** Lista todos los departamentos (paginado)
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado (lectura)
- **Códigos HTTP:** 200 OK, 401 Unauthorized
- **Ejemplo de Respuesta:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Recepción",
      "descripcion": "Área de recepción principal",
      "activo": true,
      "fecha_creacion": "2024-01-15T10:30:00Z",
      "fecha_actualizacion": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST /api/departamentos/
- **Método:** POST
- **Descripción:** Crea un nuevo departamento
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden
- **Ejemplo de Request:**
```json
{
  "nombre": "Almacén",
  "descripcion": "Área de almacenamiento",
  "activo": true
}
```

#### GET /api/departamentos/{id}/
- **Método:** GET
- **Descripción:** Obtiene el detalle de un departamento
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found

#### PATCH /api/departamentos/{id}/
- **Método:** PATCH
- **Descripción:** Actualiza parcialmente un departamento
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### PUT /api/departamentos/{id}/
- **Método:** PUT
- **Descripción:** Actualiza completamente un departamento
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### DELETE /api/departamentos/{id}/
- **Método:** DELETE
- **Descripción:** Elimina un departamento
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

---

### 3.3 Endpoints de Sensores

#### GET /api/sensores/
- **Método:** GET
- **Descripción:** Lista todos los sensores
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized

#### POST /api/sensores/
- **Método:** POST
- **Descripción:** Crea un nuevo sensor
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden
- **Ejemplo de Request:**
```json
{
  "uid": "ABC123XYZ",
  "nombre": "Tarjeta Juan Pérez",
  "estado": "activo",
  "departamento": 1,
  "usuario": null
}
```

#### GET /api/sensores/{id}/
- **Método:** GET
- **Descripción:** Obtiene el detalle de un sensor específico
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found

#### PATCH /api/sensores/{id}/
- **Método:** PATCH
- **Descripción:** Actualiza parcialmente un sensor
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Ejemplo de Request:**
```json
{
  "estado": "bloqueado"
}
```

#### PUT /api/sensores/{id}/
- **Método:** PUT
- **Descripción:** Actualiza completamente un sensor
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### DELETE /api/sensores/{id}/
- **Método:** DELETE
- **Descripción:** Elimina un sensor
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### POST /api/sensores/intentar_acceso/
- **Método:** POST
- **Descripción:** Simula un intento de acceso con un sensor RFID. Valida el sensor, verifica su estado y crea un evento de acceso.
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Ejemplo de Request:**
```json
{
  "uid": "ABC123XYZ",
  "departamento_id": 1
}
```
- **Ejemplo de Respuesta (Acceso Permitido - 200 OK):**
```json
{
  "acceso": "permitido",
  "sensor": {
    "id": 1,
    "uid": "ABC123XYZ",
    "nombre": "Tarjeta Juan Pérez",
    "estado": "activo",
    "departamento": 1,
    "departamento_nombre": "Recepción"
  },
  "evento_id": 1
}
```
- **Ejemplo de Respuesta (Acceso Denegado - Sensor no encontrado - 404 Not Found):**
```json
{
  "acceso": "denegado",
  "motivo": "Sensor no encontrado",
  "evento_id": 2
}
```
- **Ejemplo de Respuesta (Acceso Denegado - Sensor inactivo - 403 Forbidden):**
```json
{
  "acceso": "denegado",
  "motivo": "Sensor en estado: Inactivo",
  "evento_id": 3
}
```

---

### 3.4 Endpoints de Barreras

#### GET /api/barreras/
- **Método:** GET
- **Descripción:** Lista todas las barreras
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized

#### POST /api/barreras/
- **Método:** POST
- **Descripción:** Crea una nueva barrera
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden
- **Ejemplo de Request:**
```json
{
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1
}
```

#### GET /api/barreras/{id}/
- **Método:** GET
- **Descripción:** Obtiene el detalle de una barrera
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found

#### PATCH /api/barreras/{id}/
- **Método:** PATCH
- **Descripción:** Actualiza parcialmente una barrera
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### PUT /api/barreras/{id}/
- **Método:** PUT
- **Descripción:** Actualiza completamente una barrera
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### DELETE /api/barreras/{id}/
- **Método:** DELETE
- **Descripción:** Elimina una barrera
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### POST /api/barreras/{id}/abrir/
- **Método:** POST
- **Descripción:** Abre una barrera manualmente y crea un evento de apertura
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found
- **Ejemplo de Respuesta (200 OK):**
```json
{
  "mensaje": "Barrera abierta",
  "barrera": {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "abierta",
    "departamento": 1,
    "departamento_nombre": "Recepción"
  }
}
```

#### POST /api/barreras/{id}/cerrar/
- **Método:** POST
- **Descripción:** Cierra una barrera manualmente y crea un evento de cierre
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found
- **Ejemplo de Respuesta (200 OK):**
```json
{
  "mensaje": "Barrera cerrada",
  "barrera": {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "cerrada",
    "departamento": 1,
    "departamento_nombre": "Recepción"
  }
}
```

---

### 3.5 Endpoints de Eventos

#### GET /api/eventos/
- **Método:** GET
- **Descripción:** Lista todos los eventos de acceso (solo lectura, ordenados por fecha descendente)
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized
- **Ejemplo de Respuesta:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "tipo": "acceso_sensor",
      "resultado": "permitido",
      "sensor": 1,
      "sensor_uid": "ABC123XYZ",
      "sensor_nombre": "Tarjeta Juan Pérez",
      "departamento": 1,
      "departamento_nombre": "Recepción",
      "usuario": null,
      "usuario_username": null,
      "observaciones": "Acceso exitoso",
      "fecha_evento": "2024-01-15T10:35:00Z"
    }
  ]
}
```

#### GET /api/eventos/{id}/
- **Método:** GET
- **Descripción:** Obtiene el detalle de un evento específico
- **Autenticación:** Requiere token JWT
- **Permisos:** Usuario autenticado
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 404 Not Found

---

### 3.6 Endpoints de Usuarios (Solo Admin)

#### GET /api/usuarios/
- **Método:** GET
- **Descripción:** Lista todos los usuarios del sistema
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 403 Forbidden

#### POST /api/usuarios/
- **Método:** POST
- **Descripción:** Crea un nuevo usuario (solo admin puede crear usuarios)
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

#### GET /api/usuarios/{id}/
- **Método:** GET
- **Descripción:** Obtiene el detalle de un usuario
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### PATCH /api/usuarios/{id}/
- **Método:** PATCH
- **Descripción:** Actualiza parcialmente un usuario
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### PUT /api/usuarios/{id}/
- **Método:** PUT
- **Descripción:** Actualiza completamente un usuario
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### DELETE /api/usuarios/{id}/
- **Método:** DELETE
- **Descripción:** Elimina un usuario
- **Autenticación:** Requiere token JWT
- **Permisos:** Solo Admin
- **Códigos HTTP:** 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

---

## 4. Pruebas en AWS

### 4.1 Información del Despliegue

- **Plataforma:** AWS EC2
- **Instancia:** t3.micro (Free Tier)
- **Sistema Operativo:** Ubuntu Server 22.04 LTS
- **Base de Datos:** MySQL 8.0.44 (instalado directamente en EC2)
- **Servidor WSGI:** Gunicorn 22.0.0
- **Gestión de Servicio:** systemd (smartconnect.service)
- **URL Pública:** `http://18.234.1.99:8000/api/info/`
- **IP Pública:** `18.234.1.99`
- **Puerto:** 8000

**💡 Nota:** 
- La instancia t3.micro también es elegible para Free Tier y ofrece mejor rendimiento que t2.micro
- MySQL está instalado directamente en EC2 (no RDS) para optimizar costos
- El sistema funciona tanto con SQLite (desarrollo local) como MySQL (producción) según las variables de entorno
- Se utilizó **IP Elástica** (`18.234.1.99`) para mantener una dirección IP fija que no cambia al reiniciar la instancia
- Gunicorn está configurado como servicio systemd para iniciar automáticamente al reiniciar la instancia
- El servicio está habilitado y corriendo en el puerto 8000

### 4.2 Evidencias de Funcionamiento

**[AQUÍ INSERTA CAPTURAS DE PANTALLA]**

#### Captura 1: Endpoint /api/info/ funcionando desde AWS
- Muestra la respuesta JSON desde la IP pública: `http://18.234.1.99:8000/api/info/`
- Incluye la URL completa en el navegador o Postman
- Debe mostrar el JSON con autor, asignatura, proyecto, descripción y versión

#### Captura 2: Instancia EC2 corriendo
- Muestra el estado de la instancia en AWS Console
- Muestra que está "Running"

#### Captura 3: Base de datos MySQL funcionando
- Muestra conexión exitosa a MySQL (`mysql -u adminsmart -p smartconnect_db`)
- O muestra las tablas creadas (`SHOW TABLES;`)
- O muestra la estructura de una tabla (`DESCRIBE departamentos;`)

#### Captura 4: Gunicorn corriendo (Opcional)
- Muestra el estado del servicio: `sudo systemctl status smartconnect`
- O muestra los logs: `sudo journalctl -u smartconnect -f`

---

## 5. Autenticación JWT

### 5.1 Cómo Funciona el Login

El sistema utiliza **JSON Web Tokens (JWT)** para autenticación sin sesiones. Cuando un usuario hace login, el servidor genera dos tokens:

1. **Access Token (`access`)**: Token de acceso válido por **1 hora**
2. **Refresh Token (`refresh`)**: Token para renovar el access token, válido por **1 día**

### 5.2 Cómo se Genera el Token

**Proceso:**

1. Usuario envía credenciales a `/api/usuarios/login/`:
```json
{
  "username": "admin",
  "password": "password123"
}
```

2. El servidor valida las credenciales usando `authenticate()` de Django

3. Si son válidas, se genera el token usando `RefreshToken.for_user(user)`:
```python
from rest_framework_simplejwt.tokens import RefreshToken

refresh = RefreshToken.for_user(user)
access_token = refresh.access_token
```

4. El servidor retorna ambos tokens en formato JSON

### 5.3 Cómo se Envía el Token

El token se envía en el **header HTTP `Authorization`** con el formato:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Ejemplo en Postman:**
- Header Key: `Authorization`
- Header Value: `Bearer {tu_token_aqui}`

**Ejemplo con curl:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://18.234.1.99:8000/api/departamentos/
```

### 5.4 Rutas que Requieren Token

**Todas las rutas EXCEPTO:**
- `GET /api/info/` (público)
- `POST /api/usuarios/login/` (público)
- `POST /api/usuarios/registro/` (público)
- `POST /api/token/` (público)
- `POST /api/token/refresh/` (público)

**Todas las demás rutas requieren token JWT válido.**

### 5.5 Configuración de JWT

En `settings.py`:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # Token válido 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # Refresh válido 1 día
    'ROTATE_REFRESH_TOKENS': True,                    # Rota refresh token
    'BLACKLIST_AFTER_ROTATION': True,                 # Invalida token anterior
}
```

---

## 6. Manejo de Errores

### 6.1 Validaciones Implementadas

#### Validación de UID Único (Sensor)
- **Campo:** `uid` en modelo Sensor
- **Validación:** No puede haber dos sensores con el mismo UID
- **Mensaje de Error:** `"Ya existe un sensor con este UID/MAC."`
- **Código HTTP:** 400 Bad Request

#### Validación de Nombre Mínimo (Departamento, Sensor)
- **Campo:** `nombre`
- **Validación:** Mínimo 3 caracteres
- **Mensaje de Error:** `"El nombre debe tener al menos 3 caracteres."`
- **Código HTTP:** 400 Bad Request

#### Validación de Contraseñas Coincidentes (Usuario)
- **Campos:** `password` y `password_confirm`
- **Validación:** Ambos deben ser iguales
- **Mensaje de Error:** `"Las contraseñas no coinciden."`
- **Código HTTP:** 400 Bad Request

#### Validación de Estado Válido (Sensor)
- **Campo:** `estado`
- **Validación:** Debe ser uno de: activo, inactivo, bloqueado, perdido
- **Código HTTP:** 400 Bad Request

### 6.2 Mensajes de Error por Código HTTP

#### 400 Bad Request - Validación
**Ejemplo:** Crear sensor con UID duplicado
```json
{
  "uid": [
    "Ya existe un sensor con este UID/MAC."
  ]
}
```

**Ejemplo:** Crear departamento con nombre muy corto
```json
{
  "nombre": [
    "El nombre debe tener al menos 3 caracteres."
  ]
}
```

#### 401 Unauthorized - Sin Autenticación
**Ejemplo:** Acceder a endpoint protegido sin token
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

**Ejemplo:** Token inválido o expirado
```json
{
  "detail": "Token no válido o expirado",
  "code": "token_not_valid"
}
```

#### 403 Forbidden - Sin Permisos
**Ejemplo:** Operador intentando crear departamento
```json
{
  "detail": "Usted no tiene permiso para realizar esta acción."
}
```

#### 404 Not Found - Objeto No Encontrado
**Ejemplo:** Acceder a departamento inexistente
```json
{
  "detail": "No encontrado."
}
```

#### 404 Not Found - Ruta Inexistente
**Ejemplo:** Acceder a ruta que no existe
```json
{
  "error": "Ruta no encontrada",
  "detail": "La ruta solicitada no existe",
  "status_code": 404
}
```

### 6.3 Ejemplos de Respuestas de Error

**[AQUÍ INSERTA CAPTURAS DE POSTMAN MOSTRANDO ERRORES]**

- Captura de error 400 (validación)
- Captura de error 401 (sin token)
- Captura de error 403 (sin permisos)
- Captura de error 404 (no encontrado)

---

## 7. Capturas de Pruebas

### 7.1 Prueba de Login Obteniendo Token

**[INSERTA CAPTURA DE POSTMAN]**

- Request: `POST /api/usuarios/login/`
- Body con username y password
- Response mostrando `access` y `refresh` tokens
- Status Code: 200 OK

### 7.2 Prueba de Listar Datos (Un Módulo - Departamentos)

**[INSERTA CAPTURA DE POSTMAN]**

- Request: `GET /api/departamentos/`
- Header: `Authorization: Bearer {token}`
- Response con lista de departamentos
- Status Code: 200 OK

### 7.3 Prueba de Crear Datos

**[INSERTA CAPTURA DE POSTMAN]**

- Request: `POST /api/departamentos/`
- Header: `Authorization: Bearer {token}`
- Body con datos del nuevo departamento
- Response con el departamento creado
- Status Code: 201 Created

### 7.4 Prueba de Actualizar Datos

**[INSERTA CAPTURA DE POSTMAN]**

- Request: `PATCH /api/departamentos/{id}/`
- Header: `Authorization: Bearer {token}`
- Body con campos a actualizar
- Response con el departamento actualizado
- Status Code: 200 OK

### 7.5 Prueba de Eliminar Datos

**[INSERTA CAPTURA DE POSTMAN]**

- Request: `DELETE /api/departamentos/{id}/`
- Header: `Authorization: Bearer {token}`
- Response vacía
- Status Code: 204 No Content

### 7.6 Pruebas con Token Correcto

**[INSERTA CAPTURA DE POSTMAN]**

- Muestra cualquier endpoint funcionando correctamente con token válido
- Status Code: 200 OK o 201 Created

### 7.7 Pruebas Sin Token o con Errores

**[INSERTA CAPTURAS DE POSTMAN]**

- Captura 1: Request sin header Authorization → 401 Unauthorized
- Captura 2: Request con token inválido → 401 Unauthorized
- Captura 3: Operador intentando crear → 403 Forbidden
- Captura 4: Endpoint inexistente → 404 Not Found

---

## 8. Conclusiones

### 8.1 Logros Alcanzados

- ✅ API RESTful completamente funcional
- ✅ Autenticación JWT implementada y funcionando
- ✅ Sistema de permisos por roles (Admin/Operador)
- ✅ Validaciones completas en todos los modelos
- ✅ Manejo profesional de errores con códigos HTTP apropiados
- ✅ API desplegada y funcionando en AWS EC2
- ✅ Documentación completa de endpoints

### 8.2 Dificultades Encontradas

[Lista las dificultades que encontraste y cómo las resolviste]

### 8.3 Aprendizajes

[Describe qué aprendiste durante el desarrollo del proyecto]

---

## Anexos

### Anexo A: Repositorio Git

- **URL del Repositorio:** [URL de tu repositorio]
- **Rama Principal:** main/master
- **Commits:** [Número de commits realizados]

### Anexo B: Variables de Entorno

[Si quieres, puedes incluir un ejemplo de .env.example sin valores sensibles]

---

**Fin del Informe**

---

## 📝 Notas para Completar el Informe

1. ✅ **IP Pública configurada:** `18.234.1.99` (IP Elástica de AWS)
2. **Reemplaza [Tu Nombre]** con tu nombre completo
3. **Reemplaza [Tu RUT]** con tu RUT
4. **Inserta capturas de pantalla** en las secciones correspondientes:
   - Sección 4.2: Evidencias de AWS
   - Sección 6.3: Ejemplos de errores
   - Sección 7: Todas las capturas de Postman
5. **Completa las secciones de Conclusiones** con tus propias reflexiones:
   - Dificultades encontradas y cómo las resolviste
   - Aprendizajes durante el desarrollo
6. **Añade la URL de tu repositorio** en el Anexo A
7. **Verifica que todos los endpoints estén documentados** según los requerimientos
8. **Asegúrate de incluir ejemplos de JSON** para request y response de cada endpoint importante

### Cómo Tomar las Capturas

1. **Postman:**
   - Haz la petición
   - Presiona `Ctrl + Shift + 4` (Windows) o `Cmd + Shift + 4` (Mac)
   - O usa la herramienta de captura de Windows/Mac
   - Captura toda la ventana de Postman mostrando Request y Response

2. **AWS Console:**
   - Ve a EC2 → Instances
   - Captura la pantalla mostrando tu instancia "Running"

3. **Navegador:**
   - Abre `http://18.234.1.99:8000/api/info/`
   - Captura la pantalla mostrando el JSON

---

**¡Buena suerte con tu entrega! 🚀**

