# Guía: Configurar Git y Subir Proyecto a EC2

## 📋 Pasos para Configurar Git

### Paso 1: Inicializar Git Localmente

**En PowerShell (en la carpeta del proyecto):**

```powershell
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4\smartconnect_api"

# Inicializar repositorio Git
git init

# Configurar tu nombre y email (si no lo has hecho antes)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# Verificar archivos que se van a subir
git status
```

### Paso 2: Añadir Archivos al Repositorio

```powershell
# Añadir todos los archivos (excepto los que están en .gitignore)
git add .

# Ver qué archivos se añadieron
git status

# Hacer el primer commit
git commit -m "Initial commit: SmartConnect API - Proyecto Django REST Framework"
```

**✅ Verifica que NO se añadan:**
- `.env` (debe estar ignorado)
- `__pycache__/` (debe estar ignorado)
- `db.sqlite3` (debe estar ignorado)
- `venv/` (debe estar ignorado)

### Paso 3: Crear Repositorio en GitHub/GitLab

**Opción A: GitHub**

1. Ve a [GitHub.com](https://github.com)
2. Clic en **"New repository"** (o el botón **+** → **New repository**)
3. **Nombre:** `smartconnect_api`
4. **Descripción:** "API RESTful para sistema de control de acceso inteligente"
5. **Visibilidad:** Private (recomendado) o Public
6. **NO marques:** "Add a README file", "Add .gitignore", "Choose a license" (ya los tienes)
7. Clic en **"Create repository"**

**Opción B: GitLab**

1. Ve a [GitLab.com](https://gitlab.com)
2. Clic en **"New project"** → **"Create blank project"**
3. **Project name:** `smartconnect_api`
4. **Visibility Level:** Private (recomendado) o Public
5. Clic en **"Create project"**

### Paso 4: Conectar Repositorio Local con Remoto

**Después de crear el repositorio, GitHub/GitLab te dará una URL. Úsala aquí:**

```powershell
# Para GitHub (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/smartconnect_api.git

# O si prefieres SSH (necesitas configurar SSH keys primero)
# git remote add origin git@github.com:TU_USUARIO/smartconnect_api.git

# Verificar que se añadió correctamente
git remote -v
```

### Paso 5: Subir Código a GitHub/GitLab

```powershell
# Subir código (primera vez)
git branch -M main
git push -u origin main
```

**Si te pide credenciales:**
- **GitHub:** Usa un Personal Access Token (no tu contraseña)
  - Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Generate new token → Selecciona `repo` → Generate
  - Copia el token y úsalo como contraseña
- **GitLab:** Usa tu contraseña o un Personal Access Token

---

## 📥 Clonar Proyecto en EC2

### Paso 1: Instalar Git en EC2

**Conectado a EC2:**

```bash
# Instalar Git
sudo apt update
sudo apt install git -y

# Verificar instalación
git --version
```

### Paso 2: Clonar Repositorio

```bash
# Ir a la carpeta home
cd ~

# Clonar repositorio
git clone https://github.com/TU_USUARIO/smartconnect_api.git

# O si usas GitLab:
# git clone https://gitlab.com/TU_USUARIO/smartconnect_api.git

# Entrar a la carpeta del proyecto
cd smartconnect_api

# Verificar que se clonó correctamente
ls -la
```

**⚠️ IMPORTANTE:** El archivo `.env` NO estará en el repositorio (está en `.gitignore`). Debes crearlo manualmente en EC2.

### Paso 3: Crear archivo `.env` en EC2

```bash
# Crear archivo .env
nano .env
```

**Pega este contenido:**

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

**Guardar:** `Ctrl + X`, luego `Y`, luego `Enter`

---

## 🔄 Actualizar Código en EC2 (Después de Cambios)

**Cuando hagas cambios en tu computadora local:**

```powershell
# En tu computadora local
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

**En EC2:**

```bash
# Conectado a EC2
cd ~/smartconnect_api

# Actualizar código desde GitHub/GitLab
git pull origin main

# Si cambiaste requirements.txt, reinstalar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Si cambiaste modelos, aplicar migraciones
python manage.py migrate

# Reiniciar Gunicorn (si está corriendo como servicio)
sudo systemctl restart smartconnect
```

---

## ✅ Checklist

### Localmente:
- [ ] Git inicializado (`git init`)
- [ ] `.gitignore` verificado (incluye `.env`, `__pycache__`, `db.sqlite3`, `venv`)
- [ ] Primer commit realizado
- [ ] Repositorio creado en GitHub/GitLab
- [ ] Repositorio remoto conectado (`git remote add origin`)
- [ ] Código subido (`git push`)

### En EC2:
- [ ] Git instalado
- [ ] Repositorio clonado
- [ ] Archivo `.env` creado manualmente
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Migraciones aplicadas

---

## 🆘 Solución de Problemas

### Error: "fatal: not a git repository"

**Solución:** Ejecuta `git init` en la carpeta del proyecto.

### Error: "remote origin already exists"

**Solución:** 
```powershell
# Ver remotos existentes
git remote -v

# Eliminar remoto existente
git remote remove origin

# Añadir nuevo remoto
git remote add origin https://github.com/TU_USUARIO/smartconnect_api.git
```

### Error: "Permission denied" al hacer push

**Solución:** 
- Verifica que tienes permisos en el repositorio
- Usa un Personal Access Token en lugar de contraseña
- O configura SSH keys

### El archivo `.env` se subió a Git (¡PROBLEMA!)

**Solución:**
```powershell
# Eliminar del historial de Git (pero mantener el archivo local)
git rm --cached .env

# Añadir a .gitignore (si no está)
echo ".env" >> .gitignore

# Hacer commit
git commit -m "Remove .env from repository"

# Subir cambios
git push origin main
```

---

## 💡 Ventajas de Usar Git

✅ **Versionado:** Puedes ver historial de cambios  
✅ **Backup:** Tu código está en la nube  
✅ **Colaboración:** Fácil trabajar en equipo  
✅ **Actualizaciones:** Fácil actualizar código en EC2  
✅ **Rollback:** Puedes volver a versiones anteriores si algo falla  

---

**¡Listo! Con estos pasos tendrás tu proyecto en Git y podrás clonarlo en EC2.** 🎉

