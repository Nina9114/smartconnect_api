# Guía de Despliegue en AWS - SmartConnect API

## 📋 Tabla de Contenidos

1. [Requisitos según Evaluación](#requisitos-según-evaluación)
2. [Estrategia Económica para AWS](#estrategia-económica-para-aws)
3. [Preparación del Proyecto](#preparación-del-proyecto)
4. [Configuración de Base de Datos MySQL](#configuración-de-base-de-datos-mysql)
5. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
6. [Configuración para Producción](#configuración-para-producción)
7. [Despliegue en EC2](#despliegue-en-ec2)
8. [Verificación y Pruebas](#verificación-y-pruebas)

---

## Requisitos según Evaluación

Según el documento de evaluación, **DEBES cumplir:**

✅ **Despliegue en AWS (OBLIGATORIO)**
- La API debe estar disponible públicamente
- Debe entregarse: IP o dominio
- Capturas funcionando desde AWS
- **NO se aceptan proyectos solo en localhost**

✅ **Base de datos operativa**
- Debe funcionar en AWS
- Puede ser MySQL o PostgreSQL

✅ **Autenticación JWT funcionando desde AWS**

✅ **CORS configurado** para permitir peticiones externas

---

## Estrategia Económica para AWS

### Opción 1: MySQL en EC2 (MÁS ECONÓMICA) ⭐ RECOMENDADA

**Ventajas:**
- ✅ **Gratis** con tier gratuito de AWS (12 meses)
- ✅ Instalación directa en EC2 (sin RDS)
- ✅ Control total
- ✅ No consume créditos de RDS

**Desventajas:**
- Requiere configuración manual
- Debes hacer backups manuales

**Costo estimado:** $0/mes (con tier gratuito)

### Opción 2: RDS MySQL (MÁS FÁCIL pero consume créditos)

**Ventajas:**
- ✅ Configuración automática
- ✅ Backups automáticos
- ✅ Escalable

**Desventajas:**
- ❌ Consume créditos (RDS no está en tier gratuito completo)
- ❌ Más costoso a largo plazo

**Costo estimado:** ~$15-20/mes (db.t3.micro)

### ⭐ Recomendación: Opción 1 (MySQL en EC2)

Para cuidar tus créditos, usa **MySQL instalado directamente en EC2**.

---

## Preparación del Proyecto

### Paso 1: Actualizar requirements.txt

Necesitamos añadir el driver de MySQL:

```txt
Django==5.2.7
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.6.0
python-decouple==3.8
mysqlclient==2.2.0
gunicorn==21.2.0
```

**Explicación:**
- `mysqlclient`: Driver para conectar Django con MySQL
- `gunicorn`: Servidor WSGI para producción (reemplaza `runserver`)

### Paso 2: Crear archivo .env para variables de entorno

Creamos un archivo `.env` para guardar información sensible:

```env
# Django
SECRET_KEY=tu_secret_key_super_segura_aqui
DEBUG=False
ALLOWED_HOSTS=tu_ip_publica,tu-dominio.com

# Base de Datos MySQL
DB_NAME=smartconnect_db
DB_USER=smartconnect_user
DB_PASSWORD=tu_password_seguro_aqui
DB_HOST=localhost
DB_PORT=3306

# JWT (opcional, puedes dejar los valores por defecto)
JWT_ACCESS_LIFETIME_HOURS=1
JWT_REFRESH_LIFETIME_DAYS=1
```

**⚠️ IMPORTANTE:** Este archivo NO debe subirse a Git (ya está en .gitignore)

### Paso 3: Crear archivo .env.example

Creamos un ejemplo para referencia (SÍ se sube a Git):

```env
# Django
SECRET_KEY=change-this-to-a-secure-random-key
DEBUG=False
ALLOWED_HOSTS=your-ip-address,your-domain.com

# Base de Datos MySQL
DB_NAME=smartconnect_db
DB_USER=smartconnect_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306
```

---

## Configuración de Base de Datos MySQL

### Paso 1: Actualizar settings.py

Modificamos `smartconnect/settings.py` para usar variables de entorno y MySQL:

```python
from pathlib import Path
from decouple import config, Csv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='smartconnect_db'),
        'USER': config('DB_USER', default='smartconnect_user'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Si no hay variables de entorno, usar SQLite (desarrollo local)
if not config('DB_NAME', default=None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### Paso 2: Configurar CORS para producción

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:8000',
    cast=Csv()
)

# Solo permitir todos los orígenes en desarrollo
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
```

---

## Configuración de Variables de Entorno

### Paso 1: Generar SECRET_KEY seguro

En Python, ejecuta:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copia el resultado y úsalo en tu archivo `.env`.

### Paso 2: Configurar ALLOWED_HOSTS

Cuando tengas la IP pública de tu EC2, añádela al `.env`:

```env
ALLOWED_HOSTS=54.123.45.67,tu-dominio.com
```

---

## Configuración para Producción

### Paso 1: Configurar Static Files

Añade a `settings.py`:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (si necesitas subir archivos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Paso 2: Configurar Security Headers

```python
# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Si usas HTTPS (recomendado en producción)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
```

### Paso 3: Crear archivo de configuración para Gunicorn

Crea `gunicorn_config.py`:

```python
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
keepalive = 5
```

---

## Despliegue en EC2

### Paso 1: Crear Instancia EC2

1. **Ve a AWS Console** → **EC2** → **Launch Instance**
2. **Configuración:**
   - **Name:** `smartconnect-api`
   - **AMI:** Amazon Linux 2023 (Free Tier)
   - **Instance Type:** t2.micro (Free Tier)
   - **Key Pair:** Crea uno nuevo o usa existente (guarda el archivo .pem)
   - **Network Settings:** 
     - ✅ Allow HTTP traffic
     - ✅ Allow HTTPS traffic
     - Crea Security Group con:
       - Puerto 22 (SSH)
       - Puerto 80 (HTTP)
       - Puerto 443 (HTTPS)
       - Puerto 8000 (Django - temporal para pruebas)
3. **Launch Instance**

### Paso 2: Conectar a EC2

```bash
# Desde tu computadora local
ssh -i tu-archivo.pem ec2-user@tu-ip-publica
```

### Paso 3: Instalar dependencias en EC2

```bash
# Actualizar sistema
sudo yum update -y

# Instalar Python 3.11
sudo yum install python3.11 python3.11-pip -y

# Instalar MySQL Server
sudo yum install mysql-server -y

# Iniciar MySQL
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Instalar herramientas de desarrollo necesarias para mysqlclient
sudo yum install gcc python3-devel mysql-devel -y
```

### Paso 4: Configurar MySQL

**Opción A: Usando Línea de Comandos (Recomendado - Más Seguro)**

```bash
# Acceder a MySQL como root
sudo mysql

# En MySQL, ejecuta estos comandos uno por uno:
CREATE DATABASE smartconnect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'smartconnect_user'@'localhost' IDENTIFIED BY 'tu_password_seguro_aqui';
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'smartconnect_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**💡 Explicación:**
- `CREATE DATABASE`: Crea la base de datos con codificación UTF-8
- `CREATE USER`: Crea un usuario específico para tu aplicación (más seguro que usar root)
- `GRANT ALL PRIVILEGES`: Da todos los permisos al usuario sobre esa base de datos
- `FLUSH PRIVILEGES`: Aplica los cambios

**Verificar que funciona:**
```bash
# Probar conexión con el nuevo usuario
mysql -u smartconnect_user -p smartconnect_db
# Te pedirá la contraseña que definiste
# Si puedes entrar, está funcionando correctamente
# Escribe EXIT; para salir
```

---

**Opción B: Instalar phpMyAdmin (Interfaz Web - Opcional)**

Si prefieres una interfaz gráfica para administrar MySQL:

```bash
# Instalar Apache y PHP (necesarios para phpMyAdmin)
sudo yum install httpd php php-mysqlnd php-mbstring -y

# Descargar phpMyAdmin
cd /tmp
wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.tar.gz

# Extraer
tar -xzf phpMyAdmin-5.2.1-all-languages.tar.gz
sudo mv phpMyAdmin-5.2.1-all-languages /usr/share/phpmyadmin

# Configurar phpMyAdmin
sudo mkdir -p /var/lib/phpmyadmin/tmp
sudo chown -R apache:apache /var/lib/phpmyadmin
sudo chown -R apache:apache /usr/share/phpmyadmin

# Crear archivo de configuración
sudo cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php

# Generar clave secreta para phpMyAdmin
SECRET=$(openssl rand -base64 32)
sudo sed -i "s/\$cfg\['blowfish_secret'\] = '';/\$cfg['blowfish_secret'] = '$SECRET';/" /usr/share/phpmyadmin/config.inc.php

# Configurar Apache para phpMyAdmin
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

# Configurar Security Group en AWS para permitir puerto 80
# Ve a EC2 → Security Groups → Tu grupo → Inbound Rules → Add Rule
# Tipo: HTTP, Puerto: 80, Source: 0.0.0.0/0
```

**Acceder a phpMyAdmin:**
- Abre tu navegador: `http://tu-ip-publica/phpmyadmin`
- Usuario: `smartconnect_user`
- Contraseña: La que definiste al crear el usuario

**⚠️ IMPORTANTE:** phpMyAdmin expone tu base de datos en internet. Para mayor seguridad:
- Usa solo en desarrollo/pruebas
- Restringe el acceso por IP en el Security Group
- O mejor aún, usa túnel SSH (más seguro)

**Túnel SSH (Más Seguro):**
```bash
# Desde tu computadora local (Windows PowerShell)
ssh -i tu-archivo.pem -L 8888:localhost:80 ec2-user@tu-ip-publica

# Luego abre en tu navegador: http://localhost:8888/phpmyadmin
```

---

**Opción C: Usar Cliente MySQL desde tu Computadora (Recomendado para Producción)**

Puedes usar MySQL Workbench, DBeaver, o cualquier cliente MySQL desde tu PC conectándote a EC2:

1. **Configurar MySQL para aceptar conexiones remotas:**
```bash
# En EC2, editar configuración de MySQL
sudo nano /etc/my.cnf

# Añadir o modificar estas líneas:
[mysqld]
bind-address = 0.0.0.0

# Reiniciar MySQL
sudo systemctl restart mysqld
```

2. **Crear usuario con acceso remoto:**
```bash
sudo mysql
CREATE USER 'smartconnect_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'smartconnect_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

3. **Configurar Security Group:**
- Puerto 3306 (MySQL)
- Source: Tu IP pública (más seguro) o 0.0.0.0/0 (menos seguro)

4. **Conectar desde MySQL Workbench:**
- Host: Tu IP pública de EC2
- Puerto: 3306
- Usuario: smartconnect_user
- Contraseña: La que definiste

---

**⭐ Recomendación:**

Para **desarrollo y aprendizaje:** Usa **Opción A (línea de comandos)** - es más simple y suficiente.

Para **administración visual:** Usa **Opción C (cliente desde tu PC)** - más seguro que phpMyAdmin.

Para **pruebas rápidas:** Usa **Opción B (phpMyAdmin)** - pero solo con túnel SSH por seguridad.

### Paso 5: Subir tu proyecto a EC2

**Opción A: Usando Git (Recomendado)**

```bash
# En EC2
cd ~
git clone https://github.com/tu-usuario/smartconnect_api.git
cd smartconnect_api
```

**Opción B: Usando SCP**

```bash
# Desde tu computadora local
scp -i tu-archivo.pem -r smartconnect_api ec2-user@tu-ip-publica:~/
```

### Paso 6: Configurar proyecto en EC2

```bash
# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
nano .env
# Pega el contenido de tu .env con los valores correctos
# Guarda con Ctrl+X, luego Y, luego Enter

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### Paso 7: Configurar Gunicorn como servicio

Crea archivo `/etc/systemd/system/smartconnect.service`:

```ini
[Unit]
Description=SmartConnect API Gunicorn daemon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/smartconnect_api
Environment="PATH=/home/ec2-user/smartconnect_api/venv/bin"
ExecStart=/home/ec2-user/smartconnect_api/venv/bin/gunicorn \
          --config /home/ec2-user/smartconnect_api/gunicorn_config.py \
          smartconnect.wsgi:application

[Install]
WantedBy=multi-user.target
```

Iniciar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl start smartconnect
sudo systemctl enable smartconnect
sudo systemctl status smartconnect
```

### Paso 8: Configurar Nginx como Proxy Reverso (Opcional pero Recomendado)

```bash
# Instalar Nginx
sudo yum install nginx -y

# Configurar Nginx
sudo nano /etc/nginx/conf.d/smartconnect.conf
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-ip-publica;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ec2-user/smartconnect_api/staticfiles/;
    }
}
```

Iniciar Nginx:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Verificación y Pruebas

### Paso 1: Verificar que la API funciona

```bash
# Desde tu computadora local
curl http://tu-ip-publica/api/info/
```

Deberías recibir JSON con la información del proyecto.

### Paso 2: Probar desde Postman

1. Abre Postman
2. Crea un nuevo request: `GET http://tu-ip-publica/api/info/`
3. Deberías recibir respuesta 200 OK con JSON

### Paso 3: Probar autenticación

1. `POST http://tu-ip-publica/api/usuarios/login/`
2. Body: `{"username": "tu_usuario", "password": "tu_password"}`
3. Deberías recibir tokens JWT

### Paso 4: Probar endpoints protegidos

1. Usa el token obtenido en el header: `Authorization: Bearer {token}`
2. Prueba: `GET http://tu-ip-publica/api/departamentos/`
3. Deberías recibir respuesta 200 OK

---

## Checklist de Despliegue

- [ ] Instancia EC2 creada y funcionando
- [ ] MySQL instalado y configurado
- [ ] Base de datos creada
- [ ] Proyecto subido a EC2
- [ ] Variables de entorno configuradas (.env)
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado (opcional)
- [ ] Security Group configurado (puertos abiertos)
- [ ] API accesible públicamente
- [ ] Endpoint `/api/info/` funciona
- [ ] Login funciona y genera tokens
- [ ] Endpoints protegidos funcionan con token
- [ ] Capturas de pantalla tomadas para el informe

---

## Costos Estimados (Free Tier)

- **EC2 t2.micro:** $0/mes (750 horas/mes gratis por 12 meses)
- **MySQL en EC2:** $0 (incluido en EC2)
- **EBS Storage (20GB):** $0/mes (incluido en Free Tier)
- **Data Transfer:** Primeros 15GB gratis

**Total estimado: $0/mes** (dentro del Free Tier)

---

## Solución de Problemas

### Error: No se puede conectar a MySQL

```bash
# Verificar que MySQL está corriendo
sudo systemctl status mysqld

# Verificar permisos
sudo mysql -u root
SHOW GRANTS FOR 'smartconnect_user'@'localhost';
```

### Error: Gunicorn no inicia

```bash
# Ver logs
sudo journalctl -u smartconnect -f

# Verificar permisos
ls -la /home/ec2-user/smartconnect_api
```

### Error: 502 Bad Gateway

- Verifica que Gunicorn está corriendo: `sudo systemctl status smartconnect`
- Verifica que Nginx puede conectarse a Gunicorn
- Revisa logs de Nginx: `sudo tail -f /var/log/nginx/error.log`

---

## Próximos Pasos

1. **Documentar en el informe:**
   - IP pública de tu EC2
   - Capturas de pantalla de la API funcionando
   - Evidencias de pruebas desde Postman

2. **Opcional: Configurar dominio**
   - Usar Route 53 o cualquier proveedor de DNS
   - Apuntar dominio a IP de EC2

3. **Opcional: Configurar HTTPS**
   - Usar Let's Encrypt con Certbot
   - Configurar certificado SSL gratuito

---

**¡Listo para desplegar! 🚀**

