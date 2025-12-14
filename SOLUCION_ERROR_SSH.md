# Solución: Error "REMOTE HOST IDENTIFICATION HAS CHANGED"

## 🔴 Problema

Al intentar conectarte por SSH, aparece este error:
```
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
Host key verification failed.
```

## ✅ Solución Rápida

### Opción 1: Eliminar la Entrada Antigua (Recomendado)

**En PowerShell:**

```powershell
# Eliminar la entrada específica de known_hosts
ssh-keygen -R ec2-18-234-1-99.compute-1.amazonaws.com

# O eliminar por IP
ssh-keygen -R 18.234.1.99

# O eliminar la línea 39 específicamente (la que menciona el error)
# Abre el archivo y elimina la línea 39
notepad C:\Users\magdd\.ssh\known_hosts
```

**Pasos detallados:**

1. **Abre PowerShell** (como administrador si es necesario)

2. **Ejecuta este comando:**
   ```powershell
   ssh-keygen -R 18.234.1.99
   ```

3. **O ejecuta:**
   ```powershell
   ssh-keygen -R ec2-18-234-1-99.compute-1.amazonaws.com
   ```

4. **Deberías ver:** `Host 18.234.1.99 found: line 39` y luego `18.234.1.99:39 removed`

5. **Ahora intenta conectarte de nuevo:**
   ```powershell
   ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99
   ```

6. **Cuando te pregunte:** `Are you sure you want to continue connecting (yes/no/[fingerprint])?`
   - Escribe: **`yes`**
   - Presiona Enter

---

### Opción 2: Editar Manualmente known_hosts

1. **Abre el archivo known_hosts:**
   ```powershell
   notepad C:\Users\magdd\.ssh\known_hosts
   ```

2. **Busca la línea 39** (o busca `ec2-18-234-1-99` o `18.234.1.99`)

3. **Elimina esa línea completa**

4. **Guarda el archivo** (Ctrl+S)

5. **Cierra Notepad**

6. **Intenta conectarte de nuevo**

---

### Opción 3: Eliminar Todo el Archivo known_hosts (Si nada funciona)

**⚠️ Solo si las opciones anteriores no funcionan:**

```powershell
# Hacer backup (por si acaso)
Copy-Item C:\Users\magdd\.ssh\known_hosts C:\Users\magdd\.ssh\known_hosts.backup

# Eliminar el archivo
Remove-Item C:\Users\magdd\.ssh\known_hosts

# Intentar conectar de nuevo
ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99
```

---

## 🔍 ¿Por qué pasa esto?

Este error ocurre cuando:
- Te conectaste antes a otra instancia con la misma IP
- La instancia fue recreada (nueva clave SSH del servidor)
- Hay una entrada antigua en `known_hosts`

**Es normal y seguro eliminarla** - SSH te pedirá confirmar la nueva clave.

---

## ✅ Después de Solucionarlo

Una vez que elimines la entrada antigua y te conectes:

1. **SSH te preguntará:** `Are you sure you want to continue connecting (yes/no/[fingerprint])?`
2. **Escribe:** `yes`
3. **Presiona Enter**
4. **Deberías conectarte exitosamente**

**Si funciona, verás algo como:**
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux ...)
...
ubuntu@ip-xxx-xxx-xxx-xxx:~$
```

---

## 🆘 Si Aún No Funciona

### Verificar que el archivo .pem está en la ubicación correcta:

```powershell
# Verificar que el archivo existe
ls "smartconnect-key.pem"

# Si no está ahí, navega a donde lo guardaste
cd "ruta\a\tu\archivo.pem"
```

### Verificar permisos del archivo .pem:

**Si ves el error "Bad permissions" o "UNPROTECTED PRIVATE KEY FILE":**

```powershell
# Paso 1: Eliminar herencia de permisos
icacls "smartconnect-key.pem" /inheritance:r

# Paso 2: Dar solo permisos de lectura a tu usuario
icacls "smartconnect-key.pem" /grant:r "$($env:USERNAME):(R)"

# Paso 3: Verificar que quedó correcto (debe mostrar solo tu usuario)
icacls "smartconnect-key.pem"
```

**Resultado esperado:**
```
smartconnect-key.pem LAPTOP-XXXXX\tu_usuario:(R)
```

**Si aún tienes problemas, elimina todos los permisos y añade solo el tuyo:**

```powershell
# Eliminar todos los permisos
icacls "smartconnect-key.pem" /inheritance:r
icacls "smartconnect-key.pem" /remove "NT AUTHORITY\Authenticated Users"
icacls "smartconnect-key.pem" /remove "BUILTIN\Users"
icacls "smartconnect-key.pem" /remove "Everyone"

# Añadir solo tu usuario
icacls "smartconnect-key.pem" /grant:r "$($env:USERNAME):(R)"
```

### Probar con IP directa en lugar del dominio:

```powershell
ssh -i "smartconnect-key.pem" ubuntu@18.234.1.99
```

---

**¡Prueba la Opción 1 primero!** Es la más rápida y segura.

