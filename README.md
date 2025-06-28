# Microservicios API - Sistema de Gestión de Tareas

Un sistema de microservicios desarrollado en Flask que incluye autenticación, gestión de usuarios y tareas.

## Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Endpoints API](#endpoints-api)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Contribuir](#contribuir)

## Características

- **API Gateway** - Punto de entrada centralizado
- **Servicio de Autenticación** - Login, registro y validación de tokens
- **Servicio de Usuarios** - CRUD de usuarios
- **Servicio de Tareas** - Gestión completa de tareas con estados
- **Base de datos SQLite** - Almacenamiento persistente para tareas
- **Autenticación por tokens** - Seguridad basada en JWT
- **Arquitectura de microservicios** - Servicios independientes y escalables

## Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Auth Service   │    │  User Service   │
│   Puerto 5000   │────│   Puerto 5001    │    │   Puerto 5002   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         └──────────────────┐
                           │
                ┌─────────────────┐
                │  Task Service   │
                │   Puerto 5003   │
                │  (SQLite DB)    │
                └─────────────────┘
```

## Instalación

### Prerrequisitos

- Python 3.7+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/microservicios-api.git
   cd microservicios-api
   ```

2. **Instalar dependencias**
   ```bash
   pip install flask requests
   ```

3. **Estructura de archivos**
   ```
   microservicios-api/
   ├── gateway.py          # API Gateway
   ├── auth_service.py     # Servicio de autenticación  
   ├── user_service.py     # Servicio de usuarios
   ├── task_service.py     # Servicio de tareas
   ├── database.db         # Base de datos SQLite (se crea automáticamente)
   └── README.md
   ```

## Configuración

### Ejecutar los servicios

Abrir **4 terminales diferentes** y ejecutar cada servicio:

```bash
# Terminal 1 - Auth Service
python auth_service.py

# Terminal 2 - User Service  
python user_service.py

# Terminal 3 - Task Service
python task_service.py

# Terminal 4 - API Gateway
python gateway.py
```

### Puertos utilizados

- **API Gateway**: `http://127.0.0.1:5000`
- **Auth Service**: `http://127.0.0.1:5001` 
- **User Service**: `http://127.0.0.1:5002`
- **Task Service**: `http://127.0.0.1:5003`

## Uso

### 1. Autenticación

Primero debes autenticarte para obtener un token:

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "pass1"}'
```

### 2. Usar el token

Copia el token recibido y úsalo en las peticiones a tareas:

```bash
curl -X GET http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

## Endpoints API

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Registrar nuevo usuario |  |
| POST | `/auth/login` | Iniciar sesión |  |
| POST | `/auth/validate_token` | Validar token |  |
| POST | `/auth/logout` | Cerrar sesión |  |
| GET | `/auth/health` | Estado del servicio |  |

### Usuarios (`/users`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/users` | Obtener todos los usuarios |  |
| GET | `/users/{id}` | Obtener usuario por ID |  |
| POST | `/users` | Crear nuevo usuario |  |
| PUT | `/users/{id}` | Actualizar usuario |  |
| DELETE | `/users/{id}` | Eliminar usuario |  |
| GET | `/users/health` | Estado del servicio |  |

### Tareas (`/tasks`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/tasks` | Obtener todas las tareas | ✅ |
| GET | `/tasks/{id}` | Obtener tarea por ID | ✅ |
| POST | `/tasks` | Crear nueva tarea | ✅ |
| PUT | `/tasks/{id}` | Actualizar tarea | ✅ |
| DELETE | `/tasks/{id}` | Eliminar tarea (soft delete) | ✅ |
| GET | `/tasks/health` | Estado del servicio | ✅ |

### Estados de Tareas

| ID | Estado |
|----|--------|
| 1 | In progress |
| 2 | Revision |
| 3 | Completed |
| 4 | Paused |

## Ejemplos de Uso

### Crear una nueva tarea

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{
    "name_task": "Nueva Tarea",
    "desc_task": "Descripción de la tarea",
    "deadline": "2024-12-31",
    "status": 1
  }'
```

### Actualizar una tarea

```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{
    "name_task": "Tarea Actualizada",
    "status": 3
  }'
```

### Crear un nuevo usuario

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "nuevo@email.com"
  }'
```

## Usuarios Preconfigurados

### Para Autenticación:
- **Usuario**: `user1` | **Contraseña**: `pass1`
- **Usuario**: `user2` | **Contraseña**: `pass2`

### Para User Service:
- **ID 1**: `user1` | **Email**: `user1@email.com`
- **ID 2**: `user2` | **Email**: `user2@email.com`

## Pruebas con Postman

1. **Importa la colección** con todos los endpoints
2. **Configura el environment** con la variable `{{base_url}}` = `http://127.0.0.1:5000`
3. **Ejecuta el flujo**:
   - Login → Copiar token
   - Probar endpoints de usuarios
   - Probar endpoints de tareas con el token

## Solución de Problemas

### Error 415 (Unsupported Media Type)
- Agregar header `Content-Type: application/json`

### Error 401 (Unauthorized) 
- Hacer login primero para obtener token
- Incluir header `Authorization: Bearer TOKEN`

### Error 502 (Bad Gateway)
- Verificar que todos los servicios estén ejecutándose

### Error de conexión
- Verificar que los puertos no estén ocupados
- Ejecutar servicios en el orden correcto

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

### ¡Listo para usar! 
