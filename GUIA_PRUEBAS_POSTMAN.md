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

### Paso 4: Organizar con Carpetas (Opcional pero Recomendado)

Dentro de tu colección, puedes crear carpetas para organizar mejor:

1. Haz clic derecho sobre la colección **"SmartConnect API"**
2. Selecciona **"Add Folder"**
3. Crea estas carpetas:
   - **"01 - Autenticación"**
   - **"02 - Departamentos"**
   - **"03 - Sensores"**
   - **"04 - Barreras"**
   - **"05 - Eventos"**
   - **"06 - Errores"**

### Paso 5: Guardar Requests en la Colección

**Cuando creas un nuevo request:**

1. Configura el request (método, URL, headers, body)
2. Haz clic en el botón **"Save"** (arriba a la derecha) o presiona `Ctrl + S`
3. En el diálogo que aparece:
   - **Request Name:** Ponle un nombre descriptivo (ej: "Login - Obtener Token")
   - **Description:** (Opcional) Añade una descripción
   - **Select a collection or folder:** Selecciona tu colección **"SmartConnect API"**
   - **Select a folder:** (Opcional) Selecciona la carpeta correspondiente
4. Haz clic en **"Save"**

**Si ya tienes un request abierto y quieres guardarlo:**

1. Haz clic en **"Save"** o **"Save As"** (arriba a la derecha)
2. Selecciona la colección y carpeta
3. Haz clic en **"Save"**

**Para crear requests directamente en la colección:**

1. Haz clic derecho sobre la colección o carpeta
2. Selecciona **"Add Request"**
3. El request se creará automáticamente dentro de esa colección/carpeta
4. Configúralo y se guardará automáticamente

**💡 Tip:** Puedes arrastrar y soltar requests entre carpetas para reorganizarlos

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

**💡 ¿Cómo funcionan los tokens?**

Cuando haces login, recibes **automáticamente 2 tokens**:
1. **Access Token (`access`)**: Token de acceso que usas en cada petición. Expira después de **1 hora**.
2. **Refresh Token (`refresh`)**: Token especial para renovar el access token sin hacer login nuevamente. Expira después de **1 día**.

**NO necesitas crear tokens manualmente** - se generan automáticamente al hacer login.

**Flujo típico:**
1. Haces login → Obtienes `access` y `refresh`
2. Usas `access` en tus peticiones (válido por 1 hora)
3. Cuando `access` expire → Usas `refresh` para obtener un nuevo `access` (sin hacer login)
4. Si `refresh` también expira → Haces login nuevamente

---

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

**⭐ IMPORTANTE:** 
- Copia el valor de `"access"` - ese es tu token JWT de acceso
- **💾 También copia el valor de `"refresh"`** - este es tu refresh token que se genera automáticamente al hacer login

**💡 ¿Cómo obtengo el refresh token?**
- **NO necesitas crearlo manualmente** - se genera automáticamente cuando haces login
- Simplemente copia el valor de `"refresh"` de la respuesta del login
- Guárdalo en una variable de entorno en Postman (ver sección de configuración más abajo)

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

**⭐ Copia ambos valores:**
- **`"access"`** - Token de acceso (válido por 1 hora)
- **`"refresh"`** - Refresh token (válido por 1 día) - **Se genera automáticamente, no necesitas crearlo**

**💡 Nota importante:** El refresh token se obtiene automáticamente cada vez que haces login. No hay un endpoint separado para "crear" un refresh token - siempre viene junto con el access token cuando te autenticas.

---

## Prueba 2.5: Refrescar Token (Obtener Nuevo Access Token)

Cuando tu token `access` expire (después de 1 hora), puedes obtener uno nuevo usando el `refresh` token sin necesidad de hacer login nuevamente.

### Endpoint de Refresh Token

**Método:** `POST`  
**URL:** `http://localhost:8000/api/token/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "refresh": "tu_refresh_token_aqui"
}
```

**💡 Tip:** Si guardaste el refresh token en una variable de entorno llamada `refresh_token`, puedes usar:
```json
{
  "refresh": "{{refresh_token}}"
}
```

**Pasos en Postman:**

1. Selecciona método: `POST`
2. URL: `http://localhost:8000/api/token/refresh/`
3. Ve a la pestaña **"Headers"**
4. Asegúrate de tener el header:
   - **Key:** `Content-Type`
   - **Value:** `application/json`
5. Ve a la pestaña **"Body"**
6. Selecciona la opción **"raw"** (radio button)
7. En el dropdown que aparece a la derecha, selecciona **"JSON"**
8. Escribe el JSON:
   - Si guardaste el refresh token en una variable: usa `{{refresh_token}}`
   - Si no: pega el refresh token directamente reemplazando `tu_refresh_token_aqui`
9. Haz clic en **"Send"**

**Resultado Esperado:**

**Status Code:** `200 OK`

**Response Body:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**✅ Acciones después del refresh:**
1. **Copia el nuevo `access` token** - este es tu nuevo token de acceso
2. **Actualiza la variable `token` en Postman** con el nuevo valor de `access`
3. **Guarda el nuevo `refresh` token** - lo necesitarás para la próxima renovación

**💡 Consejo:** Puedes guardar también el refresh token en una variable de entorno en Postman:
- Crea una variable llamada `refresh_token` en tu entorno
- Actualiza su valor cada vez que hagas refresh

**❌ Si ves error 401 o 400:**
- Verifica que el refresh token no haya expirado (válido por 1 día)
- Verifica que el JSON esté bien formado
- Si el refresh token expiró, debes hacer login nuevamente

---

## Prueba 3: Usar Token en Peticiones

Ahora que tienes el token, lo usarás en todas las peticiones que requieren autenticación.

### Configurar Token en Postman

#### Método 1: Variable de Entorno (Recomendado)

1. En Postman, haz clic en el ícono de **"Environments"** (ojo) en la esquina superior derecha, o ve a **"Environments"** en el menú lateral izquierdo
2. Haz clic en **"+"** o **"Create Environment"** para crear un nuevo entorno
3. Nombra el entorno: **"SmartConnect Local"**
4. Añade variables en la tabla que aparece:
   
   **Variable 1: `token` (Access Token)**
   - En la primera fila de la tabla, en la columna **"Variable"** (primera columna), escribe: `token`
   - En la misma fila, en la columna **"Initial Value"** (segunda columna), déjalo vacío (este campo es opcional y no es necesario para pruebas locales)
   - En la misma fila, en la columna **"Current Value"** (tercera columna), **PEGA AQUÍ** el token que copiaste anteriormente (el valor de `"access"` que copiaste de la respuesta del login)
   - En la misma fila, en la columna **"Shared Value"** (cuarta columna), déjalo vacío (este campo es para compartir con tu equipo, no es necesario para pruebas locales)
   
   **Variable 2: `refresh_token` (Refresh Token) - Opcional pero recomendado**
   - Haz clic en **"Add"** o en una nueva fila para agregar otra variable
   - En la columna **"Variable"**, escribe: `refresh_token`
   - En **"Current Value"**, pega el valor de `"refresh"` que copiaste de la respuesta del login
   - Esto te permitirá renovar el token fácilmente cuando expire
   
   **💡 Resumen rápido:**
   - **Variable 1:** `token` → **Current Value:** (tu access token)
   - **Variable 2:** `refresh_token` → **Current Value:** (tu refresh token) - Opcional
   
   **💡 Nota:** Si tu versión de Postman solo muestra dos columnas ("Variable" y "Value"), entonces:
   - En **"Variable"**: escribe `token`
   - En **"Value"**: pega el token que copiaste (el valor de `"access"`)
   - Puedes agregar otra fila para `refresh_token` si quieres guardarlo también
   
5. Haz clic en **"Save"**
6. **IMPORTANTE:** Selecciona el entorno que acabas de crear en el dropdown de la esquina superior derecha

**Para usar la variable en requests:**
- En el header Authorization, escribe: `Bearer {{token}}`
- Postman reemplazará `{{token}}` automáticamente con el valor guardado

**Para usar el refresh token:**
- En el body JSON del endpoint `/api/token/refresh/`, escribe: `{{refresh_token}}`
- O simplemente copia y pega el valor cuando lo necesites

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

## ⚠️ IMPORTANTE: Crear Usuario Administrador

**Muchas operaciones requieren permisos de administrador.** Antes de continuar con las pruebas CRUD, asegúrate de tener un usuario con rol `admin`.

### Opción 1: Crear Superusuario y Convertirlo en Admin (Recomendado)

1. **Crea un superusuario desde la terminal:**
   ```bash
   python manage.py createsuperuser
   ```
   - Te pedirá: username, email (opcional) y password
   - Ejemplo: username: `admin`, password: `admin123`

2. **Inicia sesión en el admin de Django:**
   - Abre tu navegador y ve a: `http://localhost:8000/admin/`
   - Inicia sesión con el usuario que acabas de crear

3. **Cambia el rol a 'admin':**
   - En el admin, ve a **"Usuarios"** (Users)
   - Haz clic en tu usuario
   - En el campo **"Rol"**, selecciona **"Administrador"**
   - Haz clic en **"Guardar"**

4. **Ahora haz login desde Postman:**
   - Usa el endpoint `/api/usuarios/login/` con las credenciales del superusuario
   - El token que obtengas tendrá permisos de administrador

### Opción 2: Crear Usuario Admin desde el Admin de Django

1. **Inicia sesión en el admin:** `http://localhost:8000/admin/`
2. Ve a **"Usuarios"** → **"Añadir Usuario"**
3. Completa:
   - **Username:** (ej: `admin_test`)
   - **Password:** (elige una contraseña)
   - **Password confirmation:** (confirma la contraseña)
   - **Rol:** Selecciona **"Administrador"**
4. Haz clic en **"Guardar"**
5. Usa este usuario para hacer login en Postman

### Opción 3: Cambiar Rol de Usuario Existente

Si ya tienes un usuario creado (por ejemplo, mediante `/api/usuarios/registro/`):

1. **Inicia sesión en el admin:** `http://localhost:8000/admin/`
2. Ve a **"Usuarios"** → Busca tu usuario
3. Haz clic en tu usuario
4. En el campo **"Rol"**, cambia de **"Operador"** a **"Administrador"**
5. Haz clic en **"Guardar"**
6. **Haz login nuevamente en Postman** para obtener un nuevo token con permisos de admin

### ✅ Verificar que Eres Admin

Después de hacer login, verifica en la respuesta que el campo `"rol"` sea `"admin"`:

```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "rol": "admin",  // ← Debe decir "admin", no "operador"
    ...
  },
  "access": "...",
  "refresh": "..."
}
```

**Si dice `"rol": "operador"`, no podrás crear/editar/eliminar departamentos, sensores, etc.**

---

## Pruebas CRUD Completas

### 1. Crear un Departamento (Solo Admin)

**⚠️ REQUISITO PREVIO:** Tu usuario DEBE tener rol `admin`. Si recibes error 403, ve a la sección **[⚠️ IMPORTANTE: Crear Usuario Administrador](#-importante-crear-usuario-administrador)** más arriba.

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

**Headers:**
```
Accept: application/json
```

**⚠️ IMPORTANTE:** Agrega el header `Accept: application/json` para obtener una respuesta JSON en lugar de HTML.

**Pasos en Postman:**
1. Selecciona método: `GET`
2. URL: `http://localhost:8000/api/ruta_que_no_existe/`
3. Ve a la pestaña **"Headers"**
4. Agrega un nuevo header:
   - **Key:** `Accept`
   - **Value:** `application/json`
5. Haz clic en **"Send"**

**Resultado Esperado:**

**Status Code:** `404 Not Found`

**Response Body (JSON):**
```json
{
  "error": "Ruta no encontrada",
  "detail": "La ruta solicitada no existe",
  "status_code": 404
}
```

**💡 Nota sobre el modo DEBUG:**
- Si ves una página HTML en lugar de JSON, significa que Django está en modo `DEBUG = True`
- Esto es normal en desarrollo
- Agregar el header `Accept: application/json` fuerza a Django a devolver JSON
- En producción (con `DEBUG = False`), siempre se devolverá JSON automáticamente

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
3. Si el token expiró, puedes:
   - **Opción A:** Usar el refresh token (ve a **[Prueba 2.5: Refrescar Token](#prueba-25-refrescar-token-obtener-nuevo-access-token)**)
   - **Opción B:** Hacer login nuevamente para obtener un nuevo token

---

### Problema 3: Error 403 Forbidden - "Usted no tiene permiso para realizar esta acción"

**Causa:** No tienes permisos de administrador (tu usuario tiene rol `operador` en lugar de `admin`).

**Solución:**

1. **Verifica tu rol actual:**
   - Haz login nuevamente en Postman
   - En la respuesta, verifica el campo `"rol"` en el objeto `"user"`
   - Si dice `"rol": "operador"`, necesitas cambiarlo a `"admin"`

2. **Convierte tu usuario en administrador:**
   - Ve a la sección **[⚠️ IMPORTANTE: Crear Usuario Administrador](#-importante-crear-usuario-administrador)** más arriba en esta guía
   - Sigue las instrucciones de la **Opción 3** para cambiar el rol desde el admin de Django

3. **Después de cambiar el rol:**
   - **IMPORTANTE:** Debes hacer login nuevamente en Postman para obtener un nuevo token
   - El token anterior seguirá teniendo los permisos del rol anterior
   - Una vez que tengas un nuevo token con rol `admin`, podrás crear/editar/eliminar recursos

4. **Verifica que funcionó:**
   - En la respuesta del login, confirma que `"rol": "admin"`
   - Intenta crear un departamento nuevamente

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

**Síntoma:** Error 401 después de usar la API por un tiempo (el access token expira después de 1 hora).

**Solución:**

**Opción 1: Usar Refresh Token (Recomendado - No necesitas credenciales)**

1. Ve a la sección **[Prueba 2.5: Refrescar Token](#prueba-25-refrescar-token-obtener-nuevo-access-token)** más arriba
2. Usa el endpoint `/api/token/refresh/` con tu refresh token
3. Obtendrás un nuevo access token sin necesidad de hacer login

**Pasos rápidos:**
- **Método:** `POST`
- **URL:** `http://localhost:8000/api/token/refresh/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
  ```json
  {
    "refresh": "tu_refresh_token_aqui"
  }
  ```
- Copia el nuevo `access` token de la respuesta
- Actualiza la variable `token` en Postman con el nuevo valor

**Opción 2: Hacer Login Nuevamente**

Si tu refresh token también expiró (válido por 1 día), debes hacer login nuevamente:
1. Ve a la sección **[Prueba 2: Login y Obtención de Token](#prueba-2-login-y-obtención-de-token)**
2. Haz login con tus credenciales
3. Obtendrás nuevos tokens (access y refresh)

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

