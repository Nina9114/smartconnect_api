# Guía Simple: MySQL en EC2 (Sin phpMyAdmin)

## ✅ Decisión: Usar Solo Línea de Comandos

**Perfecto.** Esta es la opción más simple, segura y suficiente para tu proyecto.

---

## ⚠️ IMPORTANTE: Ubuntu vs Amazon Linux

**Si usaste Ubuntu Server 22.04 LTS:**
- Usuario SSH: `ubuntu` (no `ec2-user`)
- Gestor de paquetes: `apt` (no `yum`)
- Servicio MySQL: `mysql` (no `mysqld`)

**Si usaste Amazon Linux 2023:**
- Usuario SSH: `ec2-user`
- Gestor de paquetes: `yum`
- Servicio MySQL: `mysqld`

---

## Pasos para Configurar MySQL en EC2

### Paso 1: Conectarte a tu Instancia EC2

**Para Ubuntu:**
```bash
# Desde tu computadora (PowerShell o CMD)
ssh -i tu-archivo.pem ubuntu@tu-ip-publica
```

**Para Amazon Linux:**
```bash
ssh -i tu-archivo.pem ec2-user@tu-ip-publica
```

### Paso 2: Instalar MySQL

**Para Ubuntu Server 22.04 LTS:**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar MySQL Server
sudo apt install mysql-server -y

# Iniciar MySQL
sudo systemctl start mysql

# Habilitar MySQL para que inicie automáticamente al reiniciar
sudo systemctl enable mysql

# Verificar que está corriendo
sudo systemctl status mysql
```

**Para Amazon Linux 2023:**
```bash
# Actualizar sistema
sudo yum update -y

# Instalar MySQL Server
sudo yum install mysql-server -y

# Iniciar MySQL
sudo systemctl start mysqld

# Habilitar MySQL para que inicie automáticamente al reiniciar
sudo systemctl enable mysqld

# Verificar que está corriendo
sudo systemctl status mysqld
```

**✅ Deberías ver:** `Active: active (running)`

### Paso 3: Crear Base de Datos y Usuario

```bash
# Acceder a MySQL como administrador (root)
sudo mysql
```

**Ahora estás dentro de MySQL.** Verás el prompt: `mysql>`

Ejecuta estos comandos **uno por uno**:

```sql
-- Crear la base de datos
CREATE DATABASE smartconnect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para tu aplicación Django
CREATE USER 'adminsmart'@'localhost' IDENTIFIED BY 'admin123$#';

-- Dar todos los permisos al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'adminsmart'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

-- Ver las bases de datos creadas (opcional, para verificar)
SHOW DATABASES;

-- Salir de MySQL
EXIT;
```

**⚠️ IMPORTANTE - Explicación de cada parte:**

1. **`'adminsmart'`** → Nombre del usuario MySQL
   - ✅ Este es el nombre que configuraste para tu usuario
   - ⚠️ Debes usar el mismo nombre (`adminsmart`) en TODOS los comandos y en el archivo `.env`

2. **`'localhost'`** → **NO LO CAMBIES** ✅
   - Está correcto así porque Django se conecta desde la misma máquina (EC2)
   - `'localhost'` significa "desde esta misma computadora"
   - Si cambias esto, Django no podrá conectarse

3. **`'admin123$#'`** → Contraseña del usuario
   - ✅ Esta es la contraseña que configuraste
   - **Anota esta contraseña**, la necesitarás para el archivo `.env`
   - ⚠️ Asegúrate de guardarla de forma segura

### Paso 4: Verificar que Funciona

```bash
# Probar conexión con el nuevo usuario
mysql -u adminsmart -p smartconnect_db
```

- Te pedirá la contraseña (la que definiste)
- Si puedes entrar y ves el prompt `mysql>`, ¡funciona perfectamente!
- Escribe `EXIT;` para salir

---

## Configurar Variables de Entorno en Django

Una vez que tengas MySQL funcionando, configura el archivo `.env` en tu proyecto:

```env
# Base de Datos MySQL
DB_NAME=smartconnect_db
DB_USER=adminsmart
DB_PASSWORD=admin123$#
DB_HOST=localhost
DB_PORT=3306
```

Cuando Django vea `DB_NAME` configurado, automáticamente usará MySQL en lugar de SQLite.

---

## Comandos Útiles de MySQL

### Ver todas las bases de datos
```sql
SHOW DATABASES;
```

### Usar una base de datos específica
```sql
USE smartconnect_db;
```

### Ver todas las tablas
```sql
SHOW TABLES;
```

### Ver estructura de una tabla
```sql
DESCRIBE nombre_tabla;
-- Ejemplo: DESCRIBE api_sensor;
```

### Ver todos los usuarios
```sql
SELECT user, host FROM mysql.user;
```

### Ver permisos de un usuario
```sql
SHOW GRANTS FOR 'adminsmart'@'localhost';
```

### Ver datos de una tabla
```sql
SELECT * FROM nombre_tabla LIMIT 10;
-- Ejemplo: SELECT * FROM api_departamento LIMIT 10;
```

### Contar registros
```sql
SELECT COUNT(*) FROM nombre_tabla;
```

---

## Verificar que Django se Conecta Correctamente

Después de configurar el `.env` y aplicar migraciones:

```bash
# En tu proyecto Django (en EC2)
cd ~/smartconnect_api
source venv/bin/activate

# Aplicar migraciones (esto creará las tablas en MySQL)
python manage.py migrate

# Si funciona sin errores, ¡está conectado correctamente!
```

**Si ves algo como esto, está funcionando:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying api.0001_initial... OK
  ...
```

---

## Solución de Problemas

### Error: "Access denied for user"

**Causa:** Contraseña incorrecta o usuario no existe

**Solución:**
```bash
sudo mysql
# Verificar usuarios
SELECT user, host FROM mysql.user;
# Si el usuario no existe, créalo nuevamente
CREATE USER 'adminsmart'@'localhost' IDENTIFIED BY 'admin123$#';
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'adminsmart'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Error: "Can't connect to MySQL server"

**Causa:** MySQL no está corriendo

**Solución (Ubuntu):**
```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

**Solución (Amazon Linux):**
```bash
sudo systemctl start mysqld
sudo systemctl status mysqld
```

### Error: "Unknown database 'smartconnect_db'"

**Causa:** La base de datos no existe

**Solución:**
```bash
sudo mysql
CREATE DATABASE smartconnect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## ✅ Checklist

- [ ] MySQL instalado en EC2
- [ ] MySQL corriendo (`systemctl status mysql` para Ubuntu o `mysqld` para Amazon Linux)
- [ ] Base de datos `smartconnect_db` creada
- [ ] Usuario `adminsmart` creado
- [ ] Permisos otorgados al usuario
- [ ] Conexión probada (`mysql -u adminsmart -p`)
- [ ] Variables de entorno configuradas en `.env` (con `DB_USER=adminsmart` y `DB_PASSWORD=admin123$#`)
- [ ] Migraciones aplicadas (`python manage.py migrate`)

---

## 💡 Ventajas de Esta Opción

✅ **Simple:** Solo comandos básicos  
✅ **Seguro:** No expone interfaz web  
✅ **Suficiente:** Puedes hacer todo lo necesario  
✅ **Rápido:** Configuración en minutos  
✅ **Sin dependencias extra:** No necesitas Apache, PHP, etc.

---

**¡Eso es todo!** Con estos pasos tendrás MySQL funcionando perfectamente para tu proyecto Django.

