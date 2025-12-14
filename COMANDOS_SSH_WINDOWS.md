# Comandos SSH para Windows - Guía Rápida

## 🔐 Configurar Permisos del Archivo .pem

**Si recibes el error "Bad permissions" o "UNPROTECTED PRIVATE KEY FILE":**

```powershell
# Navega a la carpeta donde está tu archivo .pem
cd "D:\Magda\Magda Respaldo Antiguo\Documentos\Materias Inacap\Cuarto Semestre\Programación Back-End\Unidad 4"

# Paso 1: Eliminar herencia de permisos
icacls "smartconnect-key.pem" /inheritance:r

# Paso 2: Dar solo permisos de lectura a tu usuario
icacls "smartconnect-key.pem" /grant:r "$($env:USERNAME):(R)"

# Paso 3: Verificar permisos (debe mostrar solo tu usuario)
icacls "smartconnect-key.pem"
```

**✅ Resultado esperado:**
```
smartconnect-key.pem LAPTOP-XXXXX\tu_usuario:(R)
```

---

## 🔌 Conectarse a EC2

**Una vez que los permisos estén correctos:**

```powershell
# Opción 1: Usando IP directa (más simple)
ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99

# Opción 2: Usando dominio completo
ssh -i "smartconnect-key.pem" ubuntu@ec2-18-234-1-99.compute-1.amazonaws.com
```

**Cuando te pregunte si quieres continuar:**
- Escribe: `yes`
- Presiona Enter

---

## ✅ Verificar que Funciona

**Si la conexión es exitosa, verás:**

```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux ...)

...

ubuntu@ip-xxx-xxx-xxx-xxx:~$
```

**¡Estás conectado!** 🎉

---

## 🆘 Solución de Problemas Comunes

### Error: "Permission denied (publickey)"

**Causas posibles:**
1. Archivo .pem con permisos incorrectos → Usa los comandos de arriba
2. Usuario incorrecto → Usa `ubuntu` para Ubuntu Server, `ec2-user` para Amazon Linux
3. Archivo .pem incorrecto → Verifica que sea el correcto de tu instancia

**Solución:**
```powershell
# Verificar permisos
icacls "smartconnect-key.pem"

# Debe mostrar solo: tu_usuario:(R)
# Si muestra más usuarios, ejecuta los comandos de arriba
```

### Error: "Connection timed out"

**Causas:**
1. Instancia no está corriendo → Verifica en AWS Console
2. Security Group no tiene puerto 22 abierto → Verifica en AWS Console
3. Tu IP está bloqueada → Verifica Security Group

**Solución:**
1. Ve a AWS Console → EC2 → Instances
2. Verifica que tu instancia esté "Running"
3. Ve a Security Groups → Inbound Rules
4. Verifica que SSH (22) esté abierto para tu IP o 0.0.0.0/0

---

## 📝 Comandos Útiles una vez Conectado

```bash
# Ver información del sistema
uname -a

# Ver espacio en disco
df -h

# Ver memoria
free -h

# Ver tu ubicación actual
pwd

# Listar archivos
ls -la

# Actualizar sistema (Ubuntu)
sudo apt update && sudo apt upgrade -y
```

---

**¡Listo para continuar con la instalación de MySQL!**

