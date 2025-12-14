# Guía Paso a Paso: Crear Instancia EC2 en AWS (Cuenta Estudiante)

## 🎯 Objetivo

Crear una instancia EC2 (servidor virtual) donde desplegaremos nuestra API SmartConnect.

---

## Paso 1: Acceder a AWS Console

1. **Abre tu navegador** y ve a: https://aws.amazon.com/
2. **Haz clic en "Sign In to the Console"** (arriba a la derecha)
3. **Inicia sesión** con tus credenciales de estudiante
4. **Selecciona la región:** Recomiendo **US East (N. Virginia)** o **US East (Ohio)** para Free Tier

**💡 Tip:** La región aparece en la esquina superior derecha. Haz clic para cambiarla.

---

## Paso 2: Ir a EC2

1. En la barra de búsqueda superior, escribe: **"EC2"**
2. Haz clic en **"EC2"** (debería aparecer en los resultados)
3. O ve directamente a: https://console.aws.amazon.com/ec2/

**✅ Deberías ver:** El dashboard de EC2 con estadísticas y opciones

---

## Paso 3: Crear Instancia (Launch Instance)

1. **Haz clic en el botón naranja "Launch Instance"** (arriba a la derecha)
2. O haz clic en **"Instances"** en el menú lateral izquierdo → **"Launch Instance"**

---

## Paso 4: Configurar la Instancia

### 4.1 Nombre y Etiquetas

- **Name:** `smartconnect-api`
  - (Opcional pero recomendado: ayuda a identificar tu instancia)

### 4.2 Seleccionar AMI (Sistema Operativo)

**Busca y selecciona:**
- **Amazon Linux 2023 AMI** (Free Tier)
- O **Ubuntu Server 22.04 LTS** (Free Tier)

**💡 Recomendación:** **Amazon Linux 2023** - Es más fácil para principiantes y optimizado para AWS.

**Cómo encontrarlo:**
- En la lista de AMIs, busca "Amazon Linux 2023"
- Debe decir "Free tier eligible" ✅

### 4.3 Seleccionar Tipo de Instancia

**Selecciona:**
- **t2.micro** o **t3.micro** (Free Tier)
- Debe decir "Free tier eligible" ✅

**💡 Importante:** 
- t2.micro: 1 vCPU, 1 GB RAM (suficiente para tu proyecto)
- Gratis por 12 meses (750 horas/mes)

### 4.4 Crear o Seleccionar Key Pair

**⚠️ MUY IMPORTANTE:** Necesitas esto para conectarte a tu servidor.

**Opción A: Crear Nuevo Key Pair (Recomendado)**

1. Haz clic en **"Create new key pair"**
2. **Key pair name:** `smartconnect-key` (o el nombre que prefieras)
3. **Key pair type:** **RSA**
4. **Private key file format:** **.pem** (para Windows/Mac/Linux)
5. Haz clic en **"Create key pair"**
6. **⚠️ IMPORTANTE:** Se descargará automáticamente un archivo `.pem`
   - **Guárdalo en un lugar seguro**
   - **NO lo pierdas** - No podrás conectarte sin él
   - **NO lo subas a Git** - Es tu clave privada

**Opción B: Usar Key Pair Existente**

- Si ya tienes uno, selecciónalo del dropdown

**💡 Tip:** Guarda el archivo `.pem` en una carpeta fácil de encontrar, por ejemplo:
- `C:\Users\TuUsuario\Documents\AWS\smartconnect-key.pem`

### 4.5 Configurar Security Group (Firewall)

**Security group name:** `smartconnect-sg`

**Description:** `Security group for SmartConnect API`

**Agregar reglas de entrada (Inbound rules):**

Haz clic en **"Add security group rule"** para cada una:

1. **SSH (Puerto 22)**
   - **Type:** SSH
   - **Protocol:** TCP
   - **Port range:** 22
   - **Source:** My IP (recomendado) o 0.0.0.0/0 (menos seguro)
   - **Description:** `SSH access`

2. **HTTP (Puerto 80)**
   - **Type:** HTTP
   - **Protocol:** TCP
   - **Port range:** 80
   - **Source:** 0.0.0.0/0 (permite acceso desde internet)
   - **Description:** `HTTP access`

3. **HTTPS (Puerto 443)**
   - **Type:** HTTPS
   - **Protocol:** TCP
   - **Port range:** 443
   - **Source:** 0.0.0.0/0
   - **Description:** `HTTPS access`

4. **Custom TCP (Puerto 8000) - Para pruebas**
   - **Type:** Custom TCP
   - **Protocol:** TCP
   - **Port range:** 8000
   - **Source:** 0.0.0.0/0 (o My IP para más seguridad)
   - **Description:** `Django development server`

**💡 Explicación:**
- **Puerto 22:** Para conectarte por SSH
- **Puerto 80:** Para HTTP (si usas Nginx)
- **Puerto 443:** Para HTTPS (si configuras SSL)
- **Puerto 8000:** Para probar Django directamente (temporal)

### 4.6 Configurar Storage

- **Size (GiB):** `20` (Free Tier incluye 30GB, 20 es suficiente)
- **Volume type:** `gp3` o `gp2` (Free Tier)
- Debe decir "Free tier eligible" ✅

**💡 No cambies nada más** - Los valores por defecto están bien

### 4.7 Revisar Resumen

**Revisa que todo esté correcto:**
- ✅ AMI: Amazon Linux 2023
- ✅ Instance type: t2.micro (Free tier)
- ✅ Key pair: Tu key pair seleccionado
- ✅ Security group: Con los puertos abiertos
- ✅ Storage: 20 GB

---

## Paso 5: Lanzar la Instancia

1. **Haz clic en el botón naranja "Launch Instance"** (abajo a la derecha)
2. Espera unos segundos...
3. Deberías ver: **"Successfully initiated launch of instance i-xxxxx"**
4. Haz clic en **"View all instances"** o **"View Instances"**

---

## Paso 6: Esperar a que la Instancia Esté Lista

1. En la página de **Instances**, verás tu instancia
2. **Estado (State):** Debería cambiar de "Pending" → "Running"
3. **Estado de verificación (Status check):** Debería cambiar a "2/2 checks passed"

**⏱️ Tiempo estimado:** 1-2 minutos

**✅ Cuando veas:**
- **State:** `running` (círculo verde)
- **Status check:** `2/2 checks passed` (círculo verde)

**¡Tu instancia está lista!**

---

## Paso 7: Obtener Información Importante

### 7.1 IP Pública

1. **Selecciona tu instancia** (haz clic en el checkbox)
2. En la parte inferior, ve a la pestaña **"Details"**
3. Busca **"Public IPv4 address"**
4. **Copia esta IP** - La necesitarás para conectarte

**Ejemplo:** `54.123.45.67`

### 7.2 Verificar Security Group

1. Con tu instancia seleccionada, ve a la pestaña **"Security"**
2. Haz clic en el **Security Group** (ej: `sg-xxxxx`)
3. Verifica que las reglas estén correctas:
   - SSH (22)
   - HTTP (80)
   - HTTPS (443)
   - Custom TCP (8000)

---

## Paso 8: Conectarte a tu Instancia (SSH)

### En Windows (PowerShell o CMD)

**Opción A: Usando PowerShell (Recomendado)**

1. Abre **PowerShell**
2. Navega a donde guardaste tu archivo `.pem`:
   ```powershell
   cd C:\Users\TuUsuario\Documents\AWS
   ```

3. Cambia los permisos del archivo (solo la primera vez):
   ```powershell
   icacls smartconnect-key.pem /inheritance:r
   icacls smartconnect-key.pem /grant:r "$($env:USERNAME):(R)"
   ```

4. Conéctate:
   ```powershell
   ssh -i smartconnect-key.pem ec2-user@tu-ip-publica
   ```

   **Reemplaza:**
   - `smartconnect-key.pem` con el nombre de tu archivo
   - `tu-ip-publica` con la IP que copiaste (ej: `54.123.45.67`)

5. Si te pregunta "Are you sure you want to continue connecting?", escribe: **`yes`**

**✅ Si funciona, verás algo como:**
```
       __|  __|_  )
       _|  (     /   Amazon Linux 2023 AMI
      ___|\___|___|

[ec2-user@ip-xxx-xxx-xxx-xxx ~]$
```

**¡Estás conectado!** 🎉

---

### En Windows (Usando PuTTY - Alternativa)

Si PowerShell no funciona, puedes usar PuTTY:

1. **Descarga PuTTY:** https://www.putty.org/
2. **Descarga PuTTYgen:** (viene con PuTTY)
3. **Convierte el archivo .pem a .ppk:**
   - Abre PuTTYgen
   - Load → Selecciona tu archivo `.pem`
   - Save private key → Guarda como `.ppk`

4. **Conéctate con PuTTY:**
   - Host Name: `ec2-user@tu-ip-publica`
   - Connection type: SSH
   - Port: 22
   - En "Auth" → Credentials → Private key file: Selecciona tu `.ppk`
   - Open

---

## Paso 9: Verificar que Todo Funciona

Una vez conectado, ejecuta:

```bash
# Ver información del sistema
uname -a

# Ver espacio en disco
df -h

# Ver memoria
free -h

# Verificar que puedes instalar paquetes
sudo yum update -y
```

**✅ Si estos comandos funcionan, tu instancia está lista para usar.**

---

## Checklist de Creación

- [ ] Instancia EC2 creada
- [ ] Estado: Running
- [ ] Status check: 2/2 checks passed
- [ ] IP pública copiada
- [ ] Key pair (.pem) guardado de forma segura
- [ ] Security Group configurado con puertos necesarios
- [ ] Conexión SSH exitosa
- [ ] Puedo ejecutar comandos en la instancia

---

## 💰 Verificar Costos (Free Tier)

Para asegurarte de que estás usando Free Tier:

1. Ve a **AWS Console** → **Billing** → **Cost Explorer**
2. O ve a **EC2** → **Instances** → Selecciona tu instancia
3. Verifica que diga **"Free tier eligible"** ✅

**Recursos Free Tier que estás usando:**
- ✅ EC2 t2.micro: 750 horas/mes gratis (12 meses)
- ✅ EBS Storage: 30 GB gratis (12 meses)
- ✅ Data Transfer: 15 GB gratis (siempre)

**Costo estimado:** $0/mes (dentro del Free Tier)

---

## ⚠️ Importante: Detener la Instancia cuando No la Uses

Para **ahorrar créditos**, detén la instancia cuando no la uses:

1. Ve a **EC2** → **Instances**
2. Selecciona tu instancia
3. **Instance state** → **Stop instance**
4. Cuando quieras usarla de nuevo: **Start instance**

**💡 Nota:** 
- Al detener, pierdes la IP pública (se asigna una nueva al iniciar)
- Los datos en el disco se conservan
- No se cobra por instancias detenidas (solo por almacenamiento)

---

## 🆘 Solución de Problemas

### Error: "Permission denied (publickey)"

**Causa:** Permisos incorrectos del archivo .pem o ruta incorrecta

**Solución:**
```powershell
# En PowerShell, verifica la ruta
cd C:\ruta\a\tu\archivo.pem

# Verifica que el archivo existe
ls smartconnect-key.pem

# Cambia permisos
icacls smartconnect-key.pem /inheritance:r
icacls smartconnect-key.pem /grant:r "$($env:USERNAME):(R)"
```

### Error: "Connection timed out"

**Causa:** Security Group no tiene el puerto 22 abierto o IP bloqueada

**Solución:**
1. Ve a **EC2** → **Security Groups**
2. Selecciona tu Security Group
3. **Inbound rules** → Verifica que SSH (22) esté abierto
4. **Source** debe ser "My IP" o "0.0.0.0/0"

### Error: "Host key verification failed"

**Solución:**
```powershell
# Elimina la entrada antigua
ssh-keygen -R tu-ip-publica

# Vuelve a conectar
ssh -i smartconnect-key.pem ec2-user@tu-ip-publica
```

---

## 📝 Próximos Pasos

Una vez que tengas tu EC2 funcionando:

1. ✅ **Instalar MySQL** (ver `GUIA_MYSQL_SIMPLE.md`)
2. ✅ **Subir tu proyecto** (ver `GUIA_DESPLIEGUE_AWS.md`)
3. ✅ **Configurar variables de entorno**
4. ✅ **Aplicar migraciones**
5. ✅ **Iniciar Gunicorn**
6. ✅ **Probar desde Postman**

---

## 🎉 ¡Felicidades!

Si llegaste hasta aquí y puedes conectarte por SSH, **¡tu instancia EC2 está lista!**

**Siguiente paso:** Instalar MySQL y configurar tu proyecto Django.

---

**¿Necesitas ayuda?** Revisa la sección de "Solución de Problemas" o continúa con `GUIA_MYSQL_SIMPLE.md` para instalar MySQL.

