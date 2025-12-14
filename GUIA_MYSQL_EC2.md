# Guía Rápida: Instalar y Configurar MySQL en EC2

## 🎯 Resumen Rápido

**MySQL** es el servidor de base de datos que necesitas.  
**phpMyAdmin** es solo una herramienta opcional para administrarlo con interfaz web.

**Para tu proyecto, solo necesitas MySQL.** Puedes administrarlo desde la línea de comandos.

---

## Opción 1: MySQL con Línea de Comandos (⭐ RECOMENDADO - Más Simple)

### Paso 1: Instalar MySQL

```bash
# Conectarte a EC2
ssh -i tu-archivo.pem ec2-user@tu-ip-publica

# Instalar MySQL
sudo yum install mysql-server -y

# Iniciar MySQL
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### Paso 2: Crear Base de Datos y Usuario

```bash
# Acceder a MySQL como administrador
sudo mysql

# Ahora estás dentro de MySQL. Ejecuta estos comandos:
```

```sql
-- Crear la base de datos
CREATE DATABASE smartconnect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para tu aplicación
CREATE USER 'smartconnect_user'@'localhost' IDENTIFIED BY 'tu_password_seguro_aqui';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'smartconnect_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### Paso 3: Verificar que Funciona

```bash
# Probar conexión con el nuevo usuario
mysql -u smartconnect_user -p smartconnect_db

# Te pedirá la contraseña
# Si puedes entrar, ¡funciona perfectamente!
# Escribe EXIT; para salir
```

**✅ Listo!** Ya tienes MySQL funcionando. Django se conectará automáticamente cuando configures las variables de entorno.

---

## Opción 2: Instalar phpMyAdmin (Opcional - Solo si Quieres Interfaz Web)

### ⚠️ Advertencia de Seguridad

phpMyAdmin expone tu base de datos en internet. **Solo úsalo si:**
- Es para desarrollo/pruebas
- Usas túnel SSH (más seguro)
- O restringes el acceso por IP

### Instalación Rápida

```bash
# Instalar Apache y PHP
sudo yum install httpd php php-mysqlnd php-mbstring -y

# Descargar phpMyAdmin
cd /tmp
wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.tar.gz

# Extraer
tar -xzf phpMyAdmin-5.2.1-all-languages.tar.gz
sudo mv phpMyAdmin-5.2.1-all-languages /usr/share/phpmyadmin

# Configurar permisos
sudo mkdir -p /var/lib/phpmyadmin/tmp
sudo chown -R apache:apache /var/lib/phpmyadmin
sudo chown -R apache:apache /usr/share/phpmyadmin

# Configurar phpMyAdmin
sudo cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php

# Generar clave secreta
SECRET=$(openssl rand -base64 32)
sudo sed -i "s/\$cfg\['blowfish_secret'\] = '';/\$cfg['blowfish_secret'] = '$SECRET';/" /usr/share/phpmyadmin/config.inc.php

# Configurar Apache
sudo tee /etc/httpd/conf.d/phpmyadmin.conf > /dev/null <<EOF
Alias /phpmyadmin /usr/share/phpmyadmin
<Directory /usr/share/phpmyadmin>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
EOF

# Iniciar Apache
sudo systemctl start httpd
sudo systemctl enable httpd
```

### Acceder a phpMyAdmin de Forma Segura (Túnel SSH)

**Desde tu computadora local (Windows PowerShell):**

```bash
# Crear túnel SSH
ssh -i tu-archivo.pem -L 8888:localhost:80 ec2-user@tu-ip-publica

# Deja esta ventana abierta y abre tu navegador:
# http://localhost:8888/phpmyadmin
```

**Credenciales:**
- Usuario: `smartconnect_user`
- Contraseña: La que definiste al crear el usuario

---

## Opción 3: Usar Cliente MySQL desde tu PC (Recomendado para Producción)

Puedes usar **MySQL Workbench** o **DBeaver** desde tu computadora para conectarte a MySQL en EC2.

### Paso 1: Configurar MySQL para Conexiones Remotas

```bash
# En EC2, editar configuración
sudo nano /etc/my.cnf

# Añadir o modificar:
[mysqld]
bind-address = 0.0.0.0

# Guardar (Ctrl+X, Y, Enter)
# Reiniciar MySQL
sudo systemctl restart mysqld
```

### Paso 2: Crear Usuario con Acceso Remoto

```bash
sudo mysql

# En MySQL:
CREATE USER 'smartconnect_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'smartconnect_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 3: Configurar Security Group en AWS

1. Ve a **EC2** → **Security Groups**
2. Selecciona el Security Group de tu instancia
3. **Inbound Rules** → **Edit inbound rules** → **Add rule**
4. Configura:
   - **Type:** MySQL/Aurora
   - **Port:** 3306
   - **Source:** Tu IP pública (más seguro) o `0.0.0.0/0` (menos seguro)
5. **Save rules**

### Paso 4: Conectar desde MySQL Workbench

1. Descarga MySQL Workbench: https://dev.mysql.com/downloads/workbench/
2. Abre MySQL Workbench
3. **New Connection:**
   - **Connection Name:** SmartConnect AWS
   - **Hostname:** Tu IP pública de EC2
   - **Port:** 3306
   - **Username:** smartconnect_user
   - **Password:** (la que definiste)
4. **Test Connection** → Si funciona, **OK**

---

## Comparación de Opciones

| Opción | Facilidad | Seguridad | Recomendado Para |
|--------|-----------|-----------|------------------|
| **Línea de Comandos** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Desarrollo, Producción |
| **phpMyAdmin** | ⭐⭐⭐⭐ | ⭐⭐ | Solo desarrollo/pruebas |
| **Cliente desde PC** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Producción, Administración |

---

## ⭐ Recomendación Final

**Para tu proyecto de evaluación:**

1. **Usa Opción 1 (Línea de Comandos)** - Es suficiente y más seguro
2. Solo necesitas crear la base de datos una vez
3. Django se conectará automáticamente con las variables de entorno
4. No necesitas phpMyAdmin para nada

**Si quieres ver los datos visualmente:**
- Usa **Opción 3 (Cliente desde PC)** con MySQL Workbench
- Es más seguro que phpMyAdmin
- Puedes conectarte cuando quieras desde tu computadora

---

## Comandos Útiles de MySQL

```sql
-- Ver todas las bases de datos
SHOW DATABASES;

-- Usar una base de datos
USE smartconnect_db;

-- Ver todas las tablas
SHOW TABLES;

-- Ver estructura de una tabla
DESCRIBE nombre_tabla;

-- Ver todos los usuarios
SELECT user, host FROM mysql.user;

-- Ver permisos de un usuario
SHOW GRANTS FOR 'smartconnect_user'@'localhost';
```

---

**¡Eso es todo!** Con la Opción 1 ya tienes MySQL funcionando. Django hará el resto automáticamente cuando ejecutes las migraciones.

