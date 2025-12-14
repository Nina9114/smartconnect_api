# Guía de Pruebas en Postman - SmartConnect API

## 📋 Tabla de Contenidos

1. [Iniciar el Servidor](#iniciar-el-servidor)
2. [Configurar Postman](#configurar-postman)
3. [Prueba 1: Endpoint Público /api/info/](#prueba-1-endpoint-público-apiinfo)
4. [Prueba 2: Login y Obtención de Token](#prueba-2-login-y-obtención-de-token)
5. [Prueba 3: Usar Token en Peticiones](#prueba-3-usar-token-en-peticiones)
6. [Pruebas CRUD Completas](#pruebas-crud-completas)
7. [Solución de Problemas](#solución-de-problemas)

---

## Iniciar el Servidor

### Paso 1: Abrir Terminal

Abre PowerShell o CMD en la carpeta del proyecto:
```bash
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4\smartconnect_api"
```

### Paso 2: Iniciar el Servidor Django

```bash
python manage.py runserver
```

**Resultado esperado:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2.7, using settings 'smartconnect.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**✅ El servidor está corriendo en:** `http://127.0.0.1:8000/` o `http://localhost:8000/`

**⚠️ IMPORTANTE:** Deja esta ventana abierta mientras pruebas la API.

---

## Configurar Postman

### Paso 1: Abrir Postman

1. Abre la aplicación Postman (descárgala de [postman.com](https://www.postman.com/downloads/) si no la tienes)
2. Inicia sesión o crea una cuenta gratuita (opcional pero recomendado para guardar tus colecciones)

### Paso 2: Crear una Nueva Request

1. Haz clic en el botón **"New"** (arriba a la izquierda) o presiona `Ctrl + N`
2. Selecciona **"HTTP Request"**
3. O haz clic derecho en una colección y selecciona **"Add Request"**

### Paso 3: Crear una Colección (Recomendado)

1. Haz clic en **"New"** → **"Collection"**
2. Nombra la colección: **"SmartConnect API"**
3. Esto te ayudará a organizar todas tus pruebas

---

## Prueba 1: Endpoint Público /api/info/

### Configuración en Postman:

**Método:** `GET`  
**URL:** `http://localhost:8000/api/info/`

### Pasos:

1. **Selecciona el método:** En el dropdown izquierdo, selecciona `GET`
2. **Escribe la URL:** En el campo de URL, escribe `http://localhost:8000/api/info/`
3. **Headers:** No necesitas añadir headers (es público)
4. **Haz clic en el botón azul "Send"** (a la derecha) o presiona `Ctrl + Enter`
5. **Verifica la respuesta:** Abajo verás el Status Code (200 OK) y el Body con el JSON

### Resultado Esperado:

**Status Code:** `200 OK`

**Response Body (JSON):**
```json
{
  "autor": ["Magda"],
  "asignatura": "Programación Back End",
  "proyecto": "SmartConnect API",
  "descripcion": "API RESTful para sistema de control de acceso inteligente con sensores RFID, gestión de usuarios, departamentos y eventos de acceso",
  "version": "1.0"
}
```

**✅ Si ves esto, el servidor está funcionando correctamente.**

---

## Prueba 2: Login y Obtención de Token

Tienes **2 opciones** para hacer login:

### Opción A: Endpoint Personalizado `/api/usuarios/login/` (Recomendado)

**Método:** `POST`  
**URL:** `http://localhost:8000/api/usuarios/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "username": "tu_usuario_superusuario",
  "password": "tu_contraseña"
}
```

**Pasos en Postman:**

1. Selecciona método: `POST` (en el dropdown izquierdo)
2. URL: `http://localhost:8000/api/usuarios/login/`
3. Ve a la pestaña **"Body"** (debajo de la URL)
4. Selecciona la opción **"raw"** (radio button)
5. En el dropdown que aparece a la derecha, selecciona **"JSON"**
6. Pega el JSON de arriba en el área de texto (reemplaza `tu_usuario_superusuario` y `tu_contraseña`)
7. Haz clic en el botón azul **"Send"**

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "user": {
    "id": 1,
    "username": "tu_usuario",
    "email": "tu@email.com",
    "first_name": "",
    "last_name": "",
    "rol": "admin",
    "is_active": true
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**⭐ IMPORTANTE:** Copia el valor de `"access"` - ese es tu token JWT.

---

### Opción B: Endpoint Estándar de JWT `/api/token/`

**Método:** `POST`  
**URL:** `http://localhost:8000/api/token/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "username": "tu_usuario_superusuario",
  "password": "tu_contraseña"
}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**⭐ Copia el valor de `"access"`**

---

## Prueba 3: Usar Token en Peticiones

Ahora que tienes el token, lo usarás en todas las peticiones que requieren autenticación.

### Configurar Token en Postman

#### Método 1: Variable de Entorno (Recomendado)

1. En Postman, haz clic en el ícono de **"Environments"** (ojo) en la esquina superior derecha, o ve a **"Environments"** en el menú lateral izquierdo
2. Haz clic en **"+"** o **"Create Environment"** para crear un nuevo entorno
3. Nombra el entorno: **"SmartConnect Local"**
4. Añade una variable:
   - **Variable:** `token`
   - **Initial Value:** (déjalo vacío por ahora)
   - **Current Value:** Pega el token que copiaste (el valor de `"access"`)
5. Haz clic en **"Save"**
6. **IMPORTANTE:** Selecciona el entorno que acabas de crear en el dropdown de la esquina superior derecha

**Para usar la variable en requests:**
- En el header Authorization, escribe: `Bearer {{token}}`
- Postman reemplazará `{{token}}` automáticamente con el valor guardado

#### Método 2: Header Manual (Para pruebas rápidas)

En cada petición, añade este header manualmente:

1. Ve a la pestaña **"Headers"** (debajo de la URL)
2. Añade un nuevo header:
   - **Key:** `Authorization`
   - **Value:** `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. **⚠️ Reemplaza** `eyJ0eXAiOiJKV1QiLCJhbGc...` con tu token real

**Tip:** Puedes copiar el token directamente desde la respuesta del login haciendo clic derecho sobre el valor de `"access"` y seleccionando **"Copy"**

---

### Prueba: Listar Departamentos

**Método:** `GET`  
**URL:** `http://localhost:8000/api/departamentos/`

**Headers:**
```
Authorization: Bearer {tu_token_aqui}
```

**O si usas variable de entorno en Postman:**
```
Authorization: Bearer {{token}}
```
*(Postman reemplazará automáticamente `{{token}}` con el valor de la variable)*

**Pasos en Postman:**

1. Método: `GET` (selecciona en el dropdown)
2. URL: `http://localhost:8000/api/departamentos/`
3. Ve a la pestaña **"Headers"** (debajo de la URL)
4. Añade header:
   - **Key:** `Authorization`
   - **Value:** `Bearer {pega_tu_token_aqui}` (o `Bearer {{token}}` si usas variable de entorno)
5. Haz clic en el botón azul **"Send"**
6. Verifica que el Status Code sea `200 OK`

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

**✅ Si ves esto, la autenticación funciona correctamente.**

**❌ Si ves `401 Unauthorized`:**
- Verifica que el token esté correcto
- Verifica que el header sea: `Authorization: Bearer {token}` (con espacio después de Bearer)
- Verifica que el token no haya expirado (válido por 1 hora)

---

## Pruebas CRUD Completas

### 1. Crear un Departamento (Solo Admin)

**Método:** `POST`  
**URL:** `http://localhost:8000/api/departamentos/`

**Headers:**
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal",
  "activo": true
}
```

**Resultado Esperado:**

**Status Code:** `201 Created`

**Response Body:**
```json
{
  "id": 1,
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "fecha_actualizacion": "2024-01-15T10:30:00Z"
}
```

**✅ Guarda el `id` del departamento creado para las siguientes pruebas.**

---

### 2. Listar Departamentos

**Método:** `GET`  
**URL:** `http://localhost:8000/api/departamentos/`

**Headers:**
```
Authorization: Bearer {tu_token}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "count": 1,
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

---

### 3. Obtener Detalle de un Departamento

**Método:** `GET`  
**URL:** `http://localhost:8000/api/departamentos/1/`  
*(Reemplaza `1` con el ID del departamento que creaste)*

**Headers:**
```
Authorization: Bearer {tu_token}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "id": 1,
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "fecha_actualizacion": "2024-01-15T10:30:00Z"
}
```

---

### 4. Actualizar un Departamento (PATCH)

**Método:** `PATCH`  
**URL:** `http://localhost:8000/api/departamentos/1/`

**Headers:**
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "descripcion": "Área de recepción principal - Actualizada"
}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "id": 1,
  "nombre": "Recepción",
  "descripcion": "Área de recepción principal - Actualizada",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "fecha_actualizacion": "2024-01-15T10:31:00Z"
}
```

**Nota:** `fecha_actualizacion` cambió automáticamente.

---

### 5. Crear un Sensor

**Método:** `POST`  
**URL:** `http://localhost:8000/api/sensores/`

**Headers:**
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "uid": "ABC123XYZ",
  "nombre": "Tarjeta Juan Pérez",
  "estado": "activo",
  "departamento": 1
}
```

**Resultado Esperado:**

**Status Code:** `201 Created`

**Response Body:**
```json
{
  "id": 1,
  "uid": "ABC123XYZ",
  "nombre": "Tarjeta Juan Pérez",
  "estado": "activo",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "usuario": null,
  "usuario_username": null,
  "fecha_creacion": "2024-01-15T10:35:00Z",
  "fecha_actualizacion": "2024-01-15T10:35:00Z"
}
```

---

### 6. Simular Intento de Acceso con Sensor

**Método:** `POST`  
**URL:** `http://localhost:8000/api/sensores/intentar_acceso/`

**Headers:**
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "uid": "ABC123XYZ",
  "departamento_id": 1
}
```

**Resultado Esperado (Acceso Permitido):**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "acceso": "permitido",
  "sensor": {
    "id": 1,
    "uid": "ABC123XYZ",
    "nombre": "Tarjeta Juan Pérez",
    "estado": "activo",
    ...
  },
  "evento_id": 1
}
```

**Resultado Esperado (Acceso Denegado - Sensor no encontrado):**

**Status Code:** `404 Not Found`

**Response Body:**
```json
{
  "acceso": "denegado",
  "motivo": "Sensor no encontrado",
  "evento_id": 2
}
```

---

### 7. Crear una Barrera

**Método:** `POST`  
**URL:** `http://localhost:8000/api/barreras/`

**Headers:**
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1
}
```

**Resultado Esperado:**

**Status Code:** `201 Created`

**Response Body:**
```json
{
  "id": 1,
  "nombre": "Barrera Principal",
  "estado": "cerrada",
  "departamento": 1,
  "departamento_nombre": "Recepción",
  "fecha_actualizacion": "2024-01-15T10:40:00Z"
}
```

---

### 8. Abrir Barrera Manualmente

**Método:** `POST`  
**URL:** `http://localhost:8000/api/barreras/1/abrir/`  
*(Reemplaza `1` con el ID de la barrera)*

**Headers:**
```
Authorization: Bearer {tu_token}
```

**Body:** Vacío (no necesita body)

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "mensaje": "Barrera abierta",
  "barrera": {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "abierta",
    ...
  }
}
```

---

### 9. Cerrar Barrera Manualmente

**Método:** `POST`  
**URL:** `http://localhost:8000/api/barreras/1/cerrar/`

**Headers:**
```
Authorization: Bearer {tu_token}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "mensaje": "Barrera cerrada",
  "barrera": {
    "id": 1,
    "nombre": "Barrera Principal",
    "estado": "cerrada",
    ...
  }
}
```

---

### 10. Listar Eventos

**Método:** `GET`  
**URL:** `http://localhost:8000/api/eventos/`

**Headers:**
```
Authorization: Bearer {tu_token}
```

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "count": 3,
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
    },
    {
      "id": 2,
      "tipo": "apertura_manual",
      "resultado": "permitido",
      ...
    }
  ]
}
```

---

### 11. Probar Errores de Validación

#### Error: Crear Sensor con UID Duplicado

**Método:** `POST`  
**URL:** `http://localhost:8000/api/sensores/`

**Body:**
```json
{
  "uid": "ABC123XYZ",
  "nombre": "Otro Sensor",
  "estado": "activo",
  "departamento": 1
}
```

**Resultado Esperado:**

**Status Code:** `400 Bad Request`

**Response Body:**
```json
{
  "uid": [
    "Ya existe un sensor con este UID/MAC."
  ]
}
```

---

#### Error: Crear Departamento con Nombre Muy Corto

**Método:** `POST`  
**URL:** `http://localhost:8000/api/departamentos/`

**Body:**
```json
{
  "nombre": "AB",
  "descripcion": "Nombre muy corto"
}
```

**Resultado Esperado:**

**Status Code:** `400 Bad Request`

**Response Body:**
```json
{
  "nombre": [
    "El nombre debe tener al menos 3 caracteres."
  ]
}
```

---

### 12. Probar Sin Token (Error 401)

**Método:** `GET`  
**URL:** `http://localhost:8000/api/departamentos/`

**Headers:** (Sin Authorization)

**Resultado Esperado:**

**Status Code:** `401 Unauthorized`

**Response Body:**
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

---

### 13. Probar con Token Inválido (Error 401)

**Método:** `GET`  
**URL:** `http://localhost:8000/api/departamentos/`

**Headers:**
```
Authorization: Bearer token_invalido_12345
```

**Resultado Esperado:**

**Status Code:** `401 Unauthorized`

**Response Body:**
```json
{
  "detail": "Token no válido o expirado",
  "code": "token_not_valid"
}
```

---

### 14. Probar Ruta No Existente (Error 404)

**Método:** `GET`  
**URL:** `http://localhost:8000/api/ruta_que_no_existe/`

**Resultado Esperado:**

**Status Code:** `404 Not Found`

**Response Body:**
```json
{
  "error": "Ruta no encontrada",
  "detail": "La ruta solicitada no existe",
  "status_code": 404
}
```

---

## Solución de Problemas

### Problema 1: "Connection Refused" o "No se puede conectar"

**Causa:** El servidor Django no está corriendo.

**Solución:**
1. Abre terminal en la carpeta del proyecto
2. Ejecuta: `python manage.py runserver`
3. Verifica que veas: `Starting development server at http://127.0.0.1:8000/`

---

### Problema 2: Error 401 Unauthorized

**Causas posibles:**
- Token no incluido en el header
- Token expirado (válido por 1 hora)
- Formato incorrecto del header

**Solución:**
1. Verifica que el header sea exactamente: `Authorization: Bearer {token}`
2. Asegúrate de que haya un **espacio** después de `Bearer`
3. Obtén un nuevo token haciendo login nuevamente

---

### Problema 3: Error 403 Forbidden

**Causa:** No tienes permisos (no eres admin).

**Solución:**
1. Verifica que tu usuario tenga `rol: "admin"` en la base de datos
2. Puedes cambiarlo desde el admin de Django: `http://localhost:8000/admin/`

---

### Problema 4: Error 400 Bad Request

**Causa:** Datos inválidos en el body.

**Solución:**
1. Verifica que el Content-Type sea `application/json`
2. Verifica que el JSON esté bien formado (sin comas al final, comillas correctas)
3. Revisa los mensajes de error en la respuesta para ver qué campo está mal

---

### Problema 5: Error 404 Not Found

**Causas posibles:**
- URL incorrecta
- El objeto no existe (ej: `/api/departamentos/999/`)

**Solución:**
1. Verifica la URL (debe terminar con `/` en algunos casos)
2. Verifica que el ID del objeto exista

---

### Problema 6: Token Expirado

**Síntoma:** Error 401 después de usar la API por un tiempo.

**Solución:**
1. Haz login nuevamente para obtener un nuevo token
2. O usa el refresh token:
   - **Método:** `POST`
   - **URL:** `http://localhost:8000/api/token/refresh/`
   - **Body:** `{"refresh": "tu_refresh_token"}`

---

## Checklist de Pruebas Completas

Marca cada prueba cuando la completes:

### Endpoints Públicos
- [ ] GET `/api/info/` - Información del proyecto

### Autenticación
- [ ] POST `/api/usuarios/login/` - Login personalizado
- [ ] POST `/api/token/` - Obtener token JWT
- [ ] POST `/api/token/refresh/` - Refrescar token

### Departamentos (CRUD)
- [ ] POST `/api/departamentos/` - Crear
- [ ] GET `/api/departamentos/` - Listar
- [ ] GET `/api/departamentos/{id}/` - Detalle
- [ ] PATCH `/api/departamentos/{id}/` - Actualizar
- [ ] PUT `/api/departamentos/{id}/` - Actualizar completo
- [ ] DELETE `/api/departamentos/{id}/` - Eliminar

### Sensores (CRUD)
- [ ] POST `/api/sensores/` - Crear
- [ ] GET `/api/sensores/` - Listar
- [ ] GET `/api/sensores/{id}/` - Detalle
- [ ] PATCH `/api/sensores/{id}/` - Actualizar
- [ ] DELETE `/api/sensores/{id}/` - Eliminar
- [ ] POST `/api/sensores/intentar_acceso/` - Simular acceso

### Barreras (CRUD)
- [ ] POST `/api/barreras/` - Crear
- [ ] GET `/api/barreras/` - Listar
- [ ] GET `/api/barreras/{id}/` - Detalle
- [ ] POST `/api/barreras/{id}/abrir/` - Abrir barrera
- [ ] POST `/api/barreras/{id}/cerrar/` - Cerrar barrera

### Eventos (Solo Lectura)
- [ ] GET `/api/eventos/` - Listar
- [ ] GET `/api/eventos/{id}/` - Detalle

### Manejo de Errores
- [ ] 400 - Validación (UID duplicado, nombre corto)
- [ ] 401 - Sin token o token inválido
- [ ] 403 - Sin permisos
- [ ] 404 - Objeto no encontrado
- [ ] 404 - Ruta no existente

---

## Consejos Finales

1. **Guarda tus requests en Postman:** Crea una colección llamada "SmartConnect API" y guarda cada request dentro de carpetas organizadas (Autenticación, Departamentos, Sensores, etc.)
2. **Usa variables de entorno:** Guarda el token y la URL base (`http://localhost:8000`) como variables para facilitar el cambio entre desarrollo y producción
3. **Documenta tus requests:** En Postman puedes añadir descripciones a cada request. Haz clic en el request → pestaña "Docs" o añade una descripción en la pestaña "Description"
4. **Prueba casos límite:** No solo los casos exitosos, también los errores (400, 401, 403, 404)
5. **Verifica en el admin:** Usa `http://localhost:8000/admin/` para ver los datos creados
6. **Usa Tests en Postman:** Puedes añadir scripts de prueba automáticos. Ve a la pestaña "Tests" y añade código JavaScript para validar respuestas
7. **Exporta tu colección:** Ve a la colección → "..." → "Export" para guardar un backup de todas tus pruebas

### Atajos Útiles de Postman:
- `Ctrl + N`: Nueva request
- `Ctrl + Enter`: Enviar request
- `Ctrl + S`: Guardar request
- `Ctrl + /`: Comentar/descomentar línea en scripts

---

**¡Feliz testing! 🚀**

Si tienes problemas, revisa la sección de "Solución de Problemas" o verifica que el servidor esté corriendo correctamente.

