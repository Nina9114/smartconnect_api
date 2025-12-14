# Notas Importantes: Ubuntu Server 22.04 LTS en EC2

## ⚠️ Diferencias con Amazon Linux

Como elegiste **Ubuntu Server 22.04 LTS**, hay algunas diferencias importantes:

### 1. Usuario por Defecto

- **Amazon Linux:** `ec2-user`
- **Ubuntu:** `ubuntu` ⭐

### 2. Gestor de Paquetes

- **Amazon Linux:** `yum`
- **Ubuntu:** `apt` ⭐

### 3. Comandos de Instalación

- **Amazon Linux:** `sudo yum install paquete -y`
- **Ubuntu:** `sudo apt update && sudo apt install paquete -y` ⭐

---

## 🔧 Comandos Actualizados para Ubuntu

### Conectarte por SSH

```powershell
# En PowerShell (Windows)
ssh -i smartconnect-key.pem ubuntu@tu-ip-publica
```

**Nota:** Usa `ubuntu` en lugar de `ec2-user`

### Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### Instalar Python

```bash
# Python 3 ya viene instalado en Ubuntu 22.04
python3 --version

# Instalar pip si no está
sudo apt install python3-pip -y
```

### Instalar MySQL

```bash
# Actualizar repositorios
sudo apt update

# Instalar MySQL Server
sudo apt install mysql-server -y

# Iniciar MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Verificar estado
sudo systemctl status mysql
```

**Nota:** En Ubuntu, el servicio se llama `mysql` (no `mysqld`)

### Acceder a MySQL

```bash
# En Ubuntu, después de instalar MySQL, puedes acceder directamente como root
sudo mysql

# O si configuraste contraseña:
mysql -u root -p
```

### Instalar Dependencias para mysqlclient

```bash
# Instalar herramientas de desarrollo
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

---

## 📝 Guía Rápida: Configuración Inicial en Ubuntu

Una vez conectado a tu instancia:

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python y pip (si no están)
sudo apt install python3 python3-pip python3-venv -y

# 3. Instalar MySQL
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

# 4. Instalar dependencias para mysqlclient
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y

# 5. Instalar Git (para clonar tu repositorio)
sudo apt install git -y

# 6. Verificar instalaciones
python3 --version
mysql --version
git --version
```

---

## ✅ Todo lo Demás es Igual

- Configuración de MySQL (CREATE DATABASE, CREATE USER, etc.) es igual
- Variables de entorno (.env) son iguales
- Configuración de Django es igual
- Gunicorn funciona igual
- Todo lo demás funciona igual

---

## 🎯 Próximos Pasos

1. **Conectarte por SSH** (usando `ubuntu` como usuario)
2. **Seguir `GUIA_MYSQL_SIMPLE.md`** pero usando comandos `apt` en lugar de `yum`
3. **Seguir `GUIA_DESPLIEGUE_AWS.md`** con los ajustes de Ubuntu

---

**¡Tu instancia está lista!** Continúa con la conexión SSH usando `ubuntu` como usuario.

