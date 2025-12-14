# Información de Despliegue AWS - SmartConnect API

## 🌐 Información de la Instancia EC2

- **IP Pública (Elástica):** `18.234.1.99`
- **Tipo de Instancia:** t3.micro (Free Tier)
- **Sistema Operativo:** Ubuntu Server 22.04 LTS
- **Región:** [Especificar región de AWS si la conoces]

## 🔗 URLs de la API

### Endpoints Públicos
- **Información del Proyecto:** `http://18.234.1.99/api/info/`
- **Login:** `http://18.234.1.99/api/usuarios/login/`
- **Obtener Token JWT:** `http://18.234.1.99/api/token/`
- **Refresh Token:** `http://18.234.1.99/api/token/refresh/`

### Endpoints Protegidos (Requieren Token)
- **Departamentos:** `http://18.234.1.99/api/departamentos/`
- **Sensores:** `http://18.234.1.99/api/sensores/`
- **Barreras:** `http://18.234.1.99/api/barreras/`
- **Eventos:** `http://18.234.1.99/api/eventos/`
- **Usuarios:** `http://18.234.1.99/api/usuarios/`

## 🔐 Conexión SSH

```bash
ssh -i smartconnect-key.pem ubuntu@18.234.1.99
```

**Usuario:** `ubuntu` (porque usaste Ubuntu Server)

## 📝 Variables de Entorno (.env)

Cuando configures el archivo `.env` en EC2, usa:

```env
ALLOWED_HOSTS=18.234.1.99
```

## ✅ Ventajas de IP Elástica

- ✅ **IP fija:** No cambia al reiniciar la instancia
- ✅ **Más fácil de recordar:** Siempre la misma IP
- ✅ **Mejor para documentación:** Puedes usar la misma IP en el informe

## 🧪 Pruebas Rápidas

### Probar que la API funciona (desde tu PC):

```bash
# Endpoint público
curl http://18.234.1.99/api/info/

# Deberías recibir JSON con información del proyecto
```

### Desde Postman:

1. **GET** `http://18.234.1.99/api/info/`
2. Deberías recibir respuesta 200 OK con JSON

---

**Última actualización:** [Fecha cuando despliegues]

