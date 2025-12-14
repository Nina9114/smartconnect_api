# Checklist de Requerimientos - SmartConnect API

## ✅ Requerimientos Técnicos Obligatorios

### 1. Despliegue en AWS ✅ PREPARADO

- [x] Configuración para producción lista
- [x] Variables de entorno configuradas
- [x] Base de datos MySQL configurada
- [ ] **PENDIENTE:** Crear instancia EC2 en AWS
- [ ] **PENDIENTE:** Desplegar proyecto en EC2
- [ ] **PENDIENTE:** Obtener IP pública
- [ ] **PENDIENTE:** Tomar capturas funcionando desde AWS

**Estado:** Configuración lista, falta desplegar

---

### 2. Endpoint /api/info/ ✅ COMPLETO

- [x] Endpoint creado en `smartconnect/urls.py`
- [x] Retorna JSON con:
  - [x] autor
  - [x] asignatura
  - [x] proyecto
  - [x] descripcion
  - [x] version

**Estado:** ✅ Completado

---

### 3. Autenticación JWT ✅ COMPLETO

- [x] JWT configurado en settings.py
- [x] Endpoints de login funcionando:
  - [x] `/api/usuarios/login/` (personalizado)
  - [x] `/api/token/` (estándar)
  - [x] `/api/token/refresh/` (refresh token)
- [x] Funciona localmente
- [ ] **PENDIENTE:** Verificar que funciona desde AWS

**Estado:** ✅ Completado (falta probar en AWS)

---

### 4. Respuestas Obligatorias ✅ COMPLETO

- [x] 401 → Sin autenticación (implementado)
- [x] 403 → Sin permisos (implementado)
- [x] 400 → Validación (implementado)
- [x] 404 → Objeto no encontrado (implementado)
- [x] 404 → Ruta inexistente (handler404 personalizado)
- [x] Manejo profesional de errores

**Estado:** ✅ Completado

---

### 5. Modelos Mínimos ✅ COMPLETO

- [x] Sensor ✅
- [x] Departamento/Zona ✅
- [x] Usuario / Rol ✅
- [x] Evento ✅ (bonus)
- [x] Barrera ✅ (bonus)

**Estado:** ✅ Completado (incluso con modelos adicionales)

---

### 6. CRUD RESTful ✅ COMPLETO

- [x] GET lista (todos los modelos)
- [x] GET detalle (todos los modelos)
- [x] POST (todos los modelos)
- [x] PUT/PATCH (todos los modelos)
- [x] DELETE (todos los modelos)

**Estado:** ✅ Completado

---

### 7. Permisos ✅ COMPLETO

- [x] Admin → CRUD total
- [x] Operador → solo lectura
- [x] Permisos personalizados implementados

**Estado:** ✅ Completado

---

### 8. Validaciones Mínimas ✅ COMPLETO

- [x] MAC/UID no repetida (Sensor)
- [x] Estado válido (Sensor)
- [x] Nombre mínimo 3 caracteres (Departamento, Sensor)
- [x] Asociaciones correctas (Foreign Keys)
- [x] Contraseñas coinciden (Usuario)

**Estado:** ✅ Completado

---

### 9. Manejo Profesional de Errores ✅ COMPLETO

- [x] 400 → Validación
- [x] 401 → Sin autenticación
- [x] 403 → Sin permisos
- [x] 404 → Objeto no encontrado
- [x] 404 → Ruta inexistente (handler404)
- [x] Mensajes personalizados en JSON

**Estado:** ✅ Completado

---

### 10. Informe Técnico ⚠️ EN PROGRESO

- [x] Arquitectura general (en INFORME_TECNICO_PARTE_1.md)
- [x] Modelos y sus relaciones (en INFORME_TECNICO_PARTE_1.md)
- [ ] **PENDIENTE:** Endpoints documentados (URL, método, request/response, códigos HTTP)
- [ ] **PENDIENTE:** Pruebas desde AWS
- [ ] **PENDIENTE:** URL pública
- [ ] **PENDIENTE:** Evidencias de la API funcionando en el servidor
- [ ] **PENDIENTE:** Descripción de autenticación JWT
- [ ] **PENDIENTE:** Descripción de manejo de errores
- [ ] **PENDIENTE:** Capturas de pruebas desde Postman/Apidog

**Estado:** ⚠️ Parcialmente completado

---

## 📋 Resumen de Estado

### ✅ Completado (9/10)
1. ✅ Endpoint /api/info/
2. ✅ Autenticación JWT
3. ✅ Respuestas obligatorias
4. ✅ Modelos mínimos
5. ✅ CRUD RESTful
6. ✅ Permisos
7. ✅ Validaciones
8. ✅ Manejo de errores
9. ✅ Configuración para AWS

### ⚠️ Pendiente (1/10)
1. ⚠️ Despliegue en AWS (configuración lista, falta ejecutar)
2. ⚠️ Informe técnico completo (falta documentar endpoints y pruebas)

---

## 🎯 Próximos Pasos

### Prioridad 1: Desplegar en AWS
1. Crear instancia EC2
2. Instalar MySQL
3. Subir proyecto
4. Configurar variables de entorno
5. Aplicar migraciones
6. Iniciar Gunicorn
7. Probar desde Postman

### Prioridad 2: Completar Informe Técnico
1. Documentar todos los endpoints
2. Tomar capturas de pruebas desde AWS
3. Documentar autenticación JWT
4. Documentar manejo de errores
5. Incluir capturas de Postman

---

## 💰 Costos Estimados AWS (Free Tier)

- **EC2 t2.micro:** $0/mes (750 horas/mes gratis)
- **MySQL en EC2:** $0 (incluido)
- **EBS Storage (20GB):** $0/mes (incluido)
- **Data Transfer:** Primeros 15GB gratis

**Total: $0/mes** ✅ Perfecto para cuidar créditos

---

## 📝 Notas Importantes

1. **MySQL vs PostgreSQL:** Elegimos MySQL porque:
   - Más económico (instalado en EC2, no RDS)
   - Suficiente para el proyecto
   - Compatible con Django
   - No consume créditos de RDS

2. **Configuración Dual:** El proyecto funciona tanto con SQLite (desarrollo) como MySQL (producción) automáticamente según las variables de entorno.

3. **Seguridad:** 
   - SECRET_KEY en variables de entorno
   - DEBUG=False en producción
   - ALLOWED_HOSTS configurado
   - CORS configurado correctamente

---

**Última actualización:** 2024

