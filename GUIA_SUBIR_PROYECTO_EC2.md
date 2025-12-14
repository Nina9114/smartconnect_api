# Guía Paso a Paso: Subir Proyecto a EC2 (Ubuntu Server)

## 📋 Prerrequisitos

✅ Ya tienes:
- [x] Instancia EC2 creada (Ubuntu Server 22.04 LTS)
- [x] IP pública: `18.234.1.99`
- [x] Archivo `.pem` con permisos correctos
- [x] MySQL instalado y configurado en EC2
- [x] Usuario MySQL: `adminsmart` con contraseña `admin123$#`
- [x] Base de datos: `smartconnect_db` creada

---

## Paso 1: Conectarte a EC2

**⚠️ IMPORTANTE:** El archivo `.env` NO necesita crearse localmente. Lo crearemos directamente en EC2 después de subir el proyecto.

**Desde PowerShell en Windows:**

```powershell
# Navega a la carpeta donde está tu archivo .pem
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4"

# Conéctate a EC2
ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99
```

**✅ Si es la primera vez, escribe `yes` cuando te pregunte.**

---

## Paso 2: Instalar Python y Dependencias en EC2

**Desde PowerShell en Windows:**

```powershell
# Navega a la carpeta donde está tu archivo .pem
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4"

# Conéctate a EC2
ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99
```

**✅ Si es la primera vez, escribe `yes` cuando te pregunte.**

---

## Paso 3: Subir el Proyecto a EC2

**Una vez conectado a EC2, ejecuta estos comandos:**

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Verificar versión de Python (ya debería estar instalado)
python3 --version
# Debería mostrar: Python 3.12.3 (o similar)

# Instalar pip y venv si no están instalados
sudo apt install python3-pip python3-venv -y

# Instalar herramientas necesarias para mysqlclient
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
```

**✅ Nota:** Tu instancia tiene Python 3.12.3, que es perfecto. Django 5.2.7 es totalmente compatible con Python 3.12.

---

## Paso 4: Configurar el Proyecto en EC2

### Opción A: Usando SCP (Recomendado para empezar)

**Desde PowerShell en Windows (en una NUEVA ventana, mantén la SSH abierta):**

```powershell
# Navega a la carpeta del proyecto
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4\smartconnect_api"

# Subir todo el proyecto (excluyendo archivos innecesarios)
scp -i "..\smartconnect-key.pem" -r . ubuntu@18.234.1.99:~/smartconnect_api
```

**⚠️ Esto puede tardar unos minutos dependiendo del tamaño del proyecto.**

### Opción B: Usando Git (Si tienes repositorio)

**En EC2:**

```bash
# Instalar Git
sudo apt install git -y

# Clonar repositorio (si tienes uno)
cd ~
git clone https://github.com/tu-usuario/smartconnect_api.git
cd smartconnect_api
```

---

## Paso 5: Crear archivo `.env` en EC2

**En EC2 (en la sesión SSH):**

```bash
# Ir a la carpeta del proyecto
cd ~/smartconnect_api

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**⚠️ Si `mysqlclient` da error, instala primero las dependencias del sistema:**

```bash
# Ya las instalamos antes, pero por si acaso:
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
pip install mysqlclient
```

---

**En EC2 (después de subir el proyecto):**

```bash
# Ir a la carpeta del proyecto
cd ~/smartconnect_api

# Crear archivo .env
nano .env
```

**Pega este contenido exacto:**

```env
# Django
SECRET_KEY=django-insecure-%c$@)r)_w64p(r^(&s1=db9^=v9u&bw&@d&wp1(+(=t8*cqwyn
DEBUG=False
ALLOWED_HOSTS=18.234.1.99,localhost,127.0.0.1

# Base de Datos MySQL
DB_NAME=smartconnect_db
DB_USER=adminsmart
DB_PASSWORD=admin123$#
DB_HOST=localhost
DB_PORT=3306
```

**Para guardar en nano:**
1. Presiona `Ctrl + X`
2. Presiona `Y` (para confirmar)
3. Presiona `Enter`

**✅ Este es el ÚNICO lugar donde necesitas crear el archivo `.env` - directamente en EC2.**

---

## Paso 6: Verificar Conexión a MySQL

**En EC2:**

```bash
# Probar conexión a MySQL
mysql -u adminsmart -p smartconnect_db
# Ingresa la contraseña: admin123$#
# Si puedes entrar, escribe: EXIT;
```

**✅ Si funciona, continúa. Si no, revisa la configuración de MySQL.**

---

## Paso 7: Aplicar Migraciones

**En EC2 (con el entorno virtual activado):**

```bash
# Asegúrate de estar en la carpeta del proyecto
cd ~/smartconnect_api

# Activar entorno virtual (si no está activado)
source venv/bin/activate

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional, para admin)
python manage.py createsuperuser
# Ingresa: username, email, password

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

**✅ Si todo funciona, deberías ver las tablas creadas en MySQL.**

---

## Paso 8: Probar el Servidor (Temporal)

**En EC2:**

```bash
# Asegúrate de que el entorno virtual esté activado
source venv/bin/activate

# Iniciar servidor de desarrollo (solo para pruebas)
python manage.py runserver 0.0.0.0:8000
```

**⚠️ IMPORTANTE:** 
- Esto es solo para pruebas
- Mantén esta ventana abierta
- En otra ventana de PowerShell, prueba desde tu PC:

```powershell
# Probar desde tu computadora
curl http://18.234.1.99:8000/api/info/
```

**✅ Si funciona, verás la respuesta JSON con la información de la API.**

**Para detener el servidor:** Presiona `Ctrl + C` en EC2.

---

## Paso 9: Configurar Gunicorn (Producción)

**En EC2:**

```bash
# Verificar que gunicorn_config.py existe
ls -la gunicorn_config.py

# Si no existe, créalo:
nano gunicorn_config.py
```

**Contenido de `gunicorn_config.py`:**

```python
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
keepalive = 5
```

**Probar Gunicorn manualmente:**

```bash
# Con entorno virtual activado
source venv/bin/activate

# Iniciar Gunicorn
gunicorn --config gunicorn_config.py smartconnect.wsgi:application
```

**En otra ventana PowerShell, prueba:**

```powershell
curl http://18.234.1.99:8000/api/info/
```

**✅ Si funciona, detén Gunicorn con `Ctrl + C` y continúa.**

---

## Paso 10: Configurar Gunicorn como Servicio (systemd)

**En EC2:**

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/smartconnect.service
```

**Contenido (ajusta las rutas si es necesario):**

```ini
[Unit]
Description=SmartConnect API Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/smartconnect_api
Environment="PATH=/home/ubuntu/smartconnect_api/venv/bin"
ExecStart=/home/ubuntu/smartconnect_api/venv/bin/gunicorn \
          --config /home/ubuntu/smartconnect_api/gunicorn_config.py \
          smartconnect.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**Guardar y activar el servicio:**

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Iniciar servicio
sudo systemctl start smartconnect

# Habilitar para que inicie automáticamente al reiniciar
sudo systemctl enable smartconnect

# Ver estado
sudo systemctl status smartconnect
```

**✅ Deberías ver: `Active: active (running)`**

---

## Paso 11: Verificar que Funciona

**Desde tu computadora Windows (PowerShell):**

```powershell
# Probar endpoint de información
curl http://18.234.1.99:8000/api/info/

# Probar login (ajusta según tus credenciales)
curl -X POST http://18.234.1.99:8000/api/usuarios/login/ `
  -H "Content-Type: application/json" `
  -d '{"username":"tu_usuario","password":"tu_password"}'
```

**✅ Si funciona, ¡tu API está desplegada!**

---

## Paso 12: Configurar Security Group en AWS

**En AWS Console:**

1. Ve a **EC2** → **Security Groups**
2. Selecciona el Security Group de tu instancia
3. **Inbound Rules** → **Edit inbound rules**
4. Añade regla:
   - **Type:** Custom TCP
   - **Port:** 8000
   - **Source:** 0.0.0.0/0 (o tu IP específica para más seguridad)
   - **Description:** Django API
5. **Save rules**

---

## ✅ Checklist Final

- [ ] Proyecto subido a EC2
- [ ] Python y dependencias instaladas
- [ ] Entorno virtual creado y activado
- [ ] Archivo `.env` creado con valores correctos
- [ ] Conexión a MySQL verificada
- [ ] Migraciones aplicadas
- [ ] Gunicorn configurado como servicio
- [ ] Servicio iniciado y habilitado
- [ ] Security Group configurado (puerto 8000)
- [ ] API accesible desde internet (`http://18.234.1.99:8000/api/info/`)

---

## 🆘 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'mysqlclient'"

```bash
# Instalar dependencias del sistema
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y

# Reinstalar mysqlclient
pip install mysqlclient
```

### Error: "Access denied for user 'adminsmart'"

```bash
# Verificar que el usuario existe
sudo mysql
SELECT user, host FROM mysql.user;
# Si no existe, créalo:
CREATE USER 'adminsmart'@'localhost' IDENTIFIED BY 'admin123$#';
GRANT ALL PRIVILEGES ON smartconnect_db.* TO 'adminsmart'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Error: "Can't connect to MySQL server"

```bash
# Verificar que MySQL está corriendo
sudo systemctl status mysql

# Si no está corriendo:
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Error: Gunicorn no inicia

```bash
# Ver logs del servicio
sudo journalctl -u smartconnect -f

# Verificar que las rutas en el servicio son correctas
cat /etc/systemd/system/smartconnect.service
```

### No puedo acceder desde internet

1. Verifica Security Group (puerto 8000 abierto)
2. Verifica que Gunicorn está corriendo: `sudo systemctl status smartconnect`
3. Verifica logs: `sudo journalctl -u smartconnect -n 50`

---

## 📝 Próximos Pasos

1. **Probar todos los endpoints desde Postman**
2. **Tomar capturas para el informe técnico**
3. **Configurar Nginx como proxy reverso (opcional)**
4. **Configurar dominio (opcional)**

---

**¡Listo! Tu API debería estar funcionando en `http://18.234.1.99:8000`** 🎉

