# 🏥 OmniCare AI: Sistema de Agentes Médicos Autónomos

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Django](https://img.shields.io/badge/Django-5.0+-darkgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)


Sistema inteligente de análisis médico que combina un motor de IA basado en **LangGraph**, una capa de datos en **Django**, y una interfaz interactiva con **Streamlit**. Arquitectura de microservicios diseñada para la automatización de procesos clínicos complejos con auditoría completa y gestión profesional por roles.

---

## ✨ Nuevas Funcionalidades y Mejoras Implementadas

### 🎨 Capa de Presentación (Frontend - Streamlit)

**Header Dinámico y Contextual**
- Encabezado inteligente que detecta automáticamente el rol del usuario desde `session_state`
- Adaptación en tiempo real de la identidad visual según el contexto de operación
- Sistema de navegación contextual que muestra opciones relevantes por rol

**Diferenciación Visual por Roles**  
Sistema de colores semánticos para prevenir errores operativos:

- **🟣 Supervisor** (`#A200FF`): Tareas de administración global y auditoría de Big Data
  - Dashboard de métricas del sistema
  - Gestión completa de personal médico
  - Acceso a auditoría de consultas de IA
  - Análisis de tendencias clínicas
  
- **🔵 Médico** (`#1C83E1`): Gestión clínica operativa
  - Atención de pacientes asignados
  - Consultas asistidas por IA
  - Acceso a herramientas de diagnóstico
  - Historial de pacientes propios
  
- **🟢 Paciente** (`#28A745`): Consultas y triaje personal
  - Chat de triaje inteligente
  - Visualización de historial personal
  - Métricas de salud en tiempo real
  - Seguimiento de evolución clínica

**Diseño de Interfaz Compacto**
- Optimización CSS con `Flexbox` y `gap: 0px` para máxima legibilidad
- Tarjetas de identificación compactas mostrando DNI, Nombre y Rol
- Eliminación de espacios muertos para mejor aprovechamiento visual
- Información crítica en bloques sólidos de alta visibilidad

**Sincronización de Identificadores**
- Unificación del sistema usando `dni` como clave principal
- Coherencia total entre frontend y backend
- Manejo robusto de credenciales (DNI/Email) de forma transparente

### 🧠 Motor de Inteligencia Artificial (LangGraph)

**Grafo de Estados Robusto**
- Implementación de `StateGraph` para orquestación inteligente de agentes
- Comunicación estructurada entre nodos de recuperación, análisis y revisión ética
- Manejo de excepciones en cada etapa del flujo de trabajo
- Persistencia de contexto a través de todo el pipeline

**Capa de Auditoría Automatizada**
- Nodo de post-procesamiento que registra automáticamente cada interacción
- Envío asíncrono de síntomas y análisis de IA a Django para trazabilidad total
- Timestamp y metadatos completos de cada consulta
- Sistema de logging multinivel para debugging y compliance

**Persistencia de Contexto**
- Mejora en el manejo de `AgentState` para flujo de datos robusto
- Garantiza que `patient_id` fluya correctamente a través de todos los agentes
- Validación de integridad de datos en cada transición de estado
- Recuperación automática ante fallos de comunicación

### 🛠️ Capa de Datos (Backend - Django REST)

**Normalización de Consultas (DNI vs. Credential)**
- Corrección de errores de `FieldError` mediante unificación del campo de búsqueda
- Sistema agnóstico que acepta tanto DNI como Email en el login
- Búsqueda inteligente usando `username` como campo normalizado
- Validación robusta de credenciales con mensajes de error descriptivos

**Filtros de Seguridad Avanzados**

*Aislamiento de Médicos:*
- Modificación en el listado de facultativos para excluir al `admin/supervisor`
- Lista limpia conteniendo solo personal médico operativo
- Prevención de asignaciones incorrectas de pacientes
- Separación clara entre roles administrativos y clínicos

*Seguridad JWT:*
- Implementación de permisos `IsAuthenticated` en todos los endpoints sensibles
- Lógica de `is_staff` para proteger endpoints de historial médico
- Tokens de acceso con expiración automática
- Refresh tokens para sesiones prolongadas

**Optimización de Exportación**
- Mejora en la lógica de generación de PDFs de historiales clínicos
- Recuperación correcta de consultas filtrando por identificador único del paciente
- Formato profesional con encabezados y metadatos institucionales
- Compresión optimizada para archivos grandes

### 🔧 Arquitectura y DevOps

**Sincronización Frontend-Backend**
- Resolución del conflicto de llaves de envío en el login (`credential` vs `username`)
- Garantía de comunicación fluida entre Streamlit y Django
- Estandarización de nombres de campos en todas las capas
- Validación de contratos de datos en tiempo de desarrollo

**Documentación Técnica Evolucionada**
- Manual técnico actualizado reflejando arquitectura de microservicios
- Diagramas de flujo de la especialización en agentes autónomos
- Guías de troubleshooting por componente
- Ejemplos de uso avanzado del sistema

---

## 🚀 Guía de Inicio Rápido

Para poner en marcha el sistema completo, abre **tres terminales** y sigue estos pasos en orden:

---

### 1. Capa de Datos (Django - Puerto 8001)

Gestiona la persistencia de historiales clínicos, autenticación JWT y registros de auditoría.
```bash
# Navegar a la carpeta del proyecto Django
cd src/data-layer

# Activar entorno virtual (Windows)
venv\Scripts\activate

# O en Linux/Mac
source venv/bin/activate

# Aplicar migraciones (primera vez)
python manage.py migrate

# Crear superusuario (primera vez)
python manage.py createsuperuser

# Levantar el servicio
python manage.py runserver 8001
```

> **Importante:**  
> - Accede a `http://localhost:8001/admin` para gestionar usuarios, roles y pacientes
> - Configura al menos un usuario de cada rol (Supervisor, Médico, Paciente)
> - Asegúrate de asignar correctamente los permisos según el tipo de usuario
> - Este servicio debe estar corriendo antes de iniciar los demás componentes

---

### 2. Motor de IA (FastAPI + LangGraph - Puerto 8000)

El **"Cerebro"** que ejecuta el grafo de agentes autónomos con orquestación inteligente.
```bash
# Navegar a la carpeta donde está main.py
cd src/ai-engine

# Activar entorno virtual (Windows)
venv\Scripts\activate

# O en Linux/Mac
source venv/bin/activate

# Levantar FastAPI
python main.py

# O alternativamente con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> **Requisitos:**  
> - Archivo `.env` con tu `OPENAI_API_KEY` para usar **GPT-4o-mini**
> - Instalar dependencias: `pip install -r requirements.txt`

**Endpoints disponibles:**
- `POST /analyze` - Análisis médico estándar (respuesta completa)
- `POST /analyze-stream` - Análisis con streaming (tokens en tiempo real)
- `GET /health` - Estado del sistema y conectividad con Django

---

### 3. Dashboard Interactivo (Streamlit - Puerto 8501)

Interfaz de usuario especializada por roles con chat en tiempo real y visualización avanzada.
```bash
# Navegar a la carpeta donde está dashboard.py
cd src/dashboard

# Activar entorno virtual (Windows)
venv\Scripts\activate

# O en Linux/Mac
source venv/bin/activate

# Levantar Streamlit
streamlit run dashboard.py
```

> **Acceso:**  
> El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Funcionalidades por Rol:**

**🟣 Vista Supervisor:**
- 📊 Dashboard de métricas globales y KPIs del sistema
- 👥 Gestión completa de personal médico
- 🔍 Auditoría de todas las consultas de IA
- 📈 Análisis de Big Data sobre tendencias clínicas
- 🛠️ Configuración avanzada del sistema

**🔵 Vista Médico:**
- 👨‍⚕️ Gestión de pacientes asignados
- 💬 Chat inteligente con streaming de respuestas
- 📋 Historial completo de consultas médicas
- 📊 Visualización de evolución de pacientes
- 🔬 Herramientas de diagnóstico asistido

**🟢 Vista Paciente:**
- 🏥 Acceso a historial personal
- 💬 Chat de triaje asistido por IA
- 📈 Gráficos de métricas de salud (Dolor, Urgencia, Riesgo)
- 📅 Seguimiento de consultas anteriores
- 📄 Exportación de informes en PDF

---

## 🧪 Cómo Probar el Sistema

### Opción 1: A través del Dashboard (Recomendado)

1. Accede a `http://localhost:8501`
2. Inicia sesión con credenciales según el rol que deseas probar:
   - **Supervisor**: Usa credenciales de administrador
   - **Médico**: Usa credenciales de personal médico
   - **Paciente**: Usa credenciales de paciente
3. Explora las funcionalidades específicas de tu rol
4. En la pestaña de consulta, describe síntomas o realiza análisis
5. Observa el análisis en tiempo real con métricas actualizadas
6. Revisa el historial completo de interacciones

**Ejemplo de Flujo Completo:**
```
1. Login como Paciente (🟢)
   ↓
2. Ir a "💬 Nueva Consulta"
   ↓
3. Describir síntomas: "Dolor torácico opresivo irradiado a brazo izquierdo"
   ↓
4. Observar análisis en tiempo real con streaming
   ↓
5. Revisar métricas de triaje (Dolor: 4, Urgencia: 4, Riesgo: Alto)
   ↓
6. Consultar historial en "📋 Portal del Paciente"
```

### Opción 2: API REST con Scalar (Documentación Interactiva)

1. Asegúrate de que FastAPI esté corriendo en el puerto 8000
2. Accede a: `http://localhost:8000/scalar/v1`
3. Busca el endpoint: `POST /analyze`
4. Haz clic en **"Try it out"**
5. Usa el siguiente JSON de ejemplo:
```json
{
  "patientId": "PAC-001",
  "symptoms": "Dolor de cabeza agudo, náuseas y antecedentes de hipertensión arterial",
  "urgencyLevel": 3,
  "consentProvided": true
}
```

6. Observa la respuesta estructurada con diagnóstico, recomendaciones y métricas

> **Nota:** Scalar ofrece una interfaz más moderna que Swagger UI para explorar la API

**Documentación Alternativa:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Opción 3: Streaming de Tokens (cURL)
```bash
curl -X POST "http://localhost:8000/analyze-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": "PAC-001",
    "symptoms": "Fiebre alta 39°C, tos seca persistente y dificultad respiratoria",
    "urgencyLevel": 3,
    "consentProvided": true
  }'
```

---

## 🧠 Arquitectura de Agentes (LangGraph)

El sistema utiliza un grafo de agentes autónomos con tres nodos principales:

### 1. **Retriever Agent**
- Conecta con Django para obtener el historial clínico del paciente
- Recupera datos mediante API REST (`/api/patients/{id}/`)
- Maneja errores de conexión de forma robusta
- Cache inteligente para optimizar consultas frecuentes

### 2. **Medical Analyst Agent**
- Utiliza **GPT-4o-mini** (optimizado para costos y velocidad)
- Analiza síntomas combinados con historial médico completo
- Genera diagnósticos preliminares y recomendaciones terapéuticas
- Considera factores de riesgo y comorbilidades

### 3. **Ethics Reviewer Agent**
- Valida la seguridad de las respuestas generadas
- Registra cada interacción en la base de datos de auditoría
- Garantiza trazabilidad completa del sistema
- Filtra contenido potencialmente problemático

**Flujo de Ejecución:**
```
Consulta del Usuario
    ↓
Retriever Agent (obtiene historial)
    ↓
Medical Analyst Agent (procesa con GPT-4o-mini)
    ↓
Ethics Reviewer Agent (valida y registra)
    ↓
Respuesta al Usuario + Log de Auditoría
```

**Características Avanzadas:**
- ✅ Manejo de estado robusto con `AgentState`
- ✅ Persistencia de contexto entre agentes
- ✅ Recuperación automática ante fallos
- ✅ Logging detallado para debugging
- ✅ Streaming de respuestas en tiempo real

---

## 📊 Arquitectura Técnica

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Frontend** | Streamlit | Dashboard interactivo con roles y visualización de métricas |
| **Orquestador** | LangGraph | Grafo de agentes autónomos y gestión de estado |
| **Backend** | Django 5.0 | Persistencia, seguridad JWT y lógica de negocio |
| **IA Model** | GPT-4o-mini | Procesamiento de lenguaje natural y análisis clínico |
| **API Layer** | FastAPI | Endpoint de alto rendimiento para streaming de IA |
| **Base de Datos** | SQLite/PostgreSQL | Almacenamiento de historiales y auditoría |
| **Visualización** | Matplotlib | Gráficos y métricas en tiempo real |
| **Documentación** | Swagger UI + Scalar | API Explorer interactivo |

### Diagrama de Flujo de Datos
```
┌─────────────────┐
│  Usuario (Rol)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Streamlit Dashboard    │
│  (Header Dinámico)      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  FastAPI Endpoint       │
│  POST /analyze-stream   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  LangGraph StateGraph   │
│  ┌─────────────────┐    │
│  │ Retriever Agent │    │
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │ Analyst Agent   │    │
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │ Ethics Reviewer │    │
│  └────────┬────────┘    │
└───────────┼─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Django REST API        │
│  - Auditoría            │
│  - Historial            │
│  - Autenticación JWT    │
└─────────────────────────┘
```

---

## 🔒 Seguridad y Auditoría Especializada

### Características de Seguridad

- ✅ **Autenticación JWT**: Tokens seguros para comunicación entre microservicios
- ✅ **Validación Ética Obligatoria**: Filtro automático antes de entregar diagnósticos
- ✅ **Trazabilidad Completa**: Cada interacción genera un log consultable por Supervisores
- ✅ **Gestión de Roles Granular**: Permisos específicos por tipo de usuario
- ✅ **Consentimiento Explícito**: Requerido para todos los análisis médicos
- ✅ **Aislamiento de Datos**: Pacientes solo ven su información, médicos solo sus pacientes
- ✅ **Cifrado en Tránsito**: HTTPS para todas las comunicaciones

### Sistema de Auditoría

**Registros Almacenados:**
- ✏️ Timestamp de la consulta
- 👤 Usuario que realizó la acción (DNI/Nombre)
- 🏥 Paciente involucrado (ID único)
- 📝 Síntomas reportados (texto completo)
- 🤖 Análisis completo generado por la IA
- 📊 Métricas de triaje (dolor, urgencia, riesgo)
- ✅ Resultado de la validación ética
- 🔍 Metadata del sistema (versión, modelo usado)

**Acceso a Auditoría:**
- Solo disponible para usuarios con rol **Supervisor** (🟣)
- Búsqueda y filtrado avanzado por:
  - Fecha y rango de tiempo
  - Usuario específico
  - Paciente específico
  - Nivel de urgencia
  - Métricas de riesgo
- Exportación de reportes en PDF/CSV para cumplimiento normativo
- Dashboard de métricas agregadas

---

## 📋 Requisitos del Sistema

### Dependencias Principales
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

**Librerías Esenciales:**
```txt
# Orquestación de Agentes
langgraph>=0.0.20
langchain-openai>=0.0.5
langchain-core>=0.1.10

# API y Servidor
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
django>=5.0.0
djangorestframework>=3.14.0

# Interfaz de Usuario
streamlit>=1.30.0

# Seguridad
pyjwt>=2.8.0
cryptography>=41.0.0

# Utilidades
httpx>=0.26.0
python-dotenv>=1.0.0
matplotlib>=3.8.0
reportlab>=4.0.0  # Para generación de PDFs
```

---

## 🔧 Configuración del Entorno

### Variables de Entorno Requeridas (.env)
```env
# OpenAI Configuration
OPENAI_API_KEY=tu-api-key-aqui

# Django Configuration
DJANGO_SECRET_KEY=tu-secret-key-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (opcional, por defecto usa SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/omnicare

# JWT Configuration
JWT_SECRET_KEY=tu-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
```

### Puertos Utilizados

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Django Backend | `8001` | API REST y capa de datos |
| FastAPI Motor IA | `8000` | Orquestador de agentes |
| Streamlit Dashboard | `8501` | Interfaz de usuario |

---

## 🎯 Próximos Pasos y Roadmap

### En Desarrollo
- [ ] Dashboard de métricas avanzadas para Supervisores con KPIs en tiempo real
- [ ] Sistema de notificaciones push para alertas críticas de pacientes
- [ ] Integración con sistemas de historia clínica electrónica (HCE/EHR)
- [ ] Soporte multilenguaje (inglés, portugués)
- [ ] Modo offline para áreas con conectividad limitada

### Futuras Mejoras
- [ ] Módulo de telemedicina con videollamadas integradas
- [ ] Sistema de citas automatizado con recordatorios
- [ ] Análisis predictivo con machine learning para detección temprana
- [ ] App móvil nativa para iOS y Android
- [ ] Integración con dispositivos wearables para monitoreo continuo
- [ ] Sistema de segunda opinión médica colaborativa

---

## 📚 Documentación Adicional

### URLs de Documentación del Sistema

- **Scalar API Explorer**: `http://localhost:8000/scalar/v1`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Django Admin**: `http://localhost:8001/admin`
- **Streamlit Dashboard**: `http://localhost:8501`

### Estructura del Proyecto
```
omnicare-ai/
├── src/
│   ├── data-layer/          # Django backend
│   │   ├── api/             # REST API endpoints
│   │   │   ├── views.py     # Vistas y lógica de negocio
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   ├── models/          # Modelos de datos
│   │   │   ├── patient.py
│   │   │   ├── consultation.py
│   │   │   └── audit.py
│   │   ├── migrations/      # Migraciones de base de datos
│   │   └── manage.py
│   │
│   ├── ai-engine/           # FastAPI + LangGraph
│   │   ├── main.py          # Servidor FastAPI
│   │   ├── agents/          # Agentes autónomos
│   │   │   ├── retriever.py
│   │   │   ├── analyst.py
│   │   │   └── ethics.py
│   │   ├── graph.py         # StateGraph definition
│   │   └── config.py        # Configuración del motor
│   │
│   └── dashboard/           # Streamlit UI
│       ├── dashboard.py     # Aplicación principal
│       ├── components/      # Componentes reutilizables
│       │   ├── header.py
│       │   ├── chat.py
│       │   └── metrics.py
│       └── utils/           # Utilidades
│
├── tests/                   # Tests automatizados
│   ├── test_agents.py
│   ├── test_api.py
│   └── test_integration.py
│
├── docs/                    # Documentación técnica
│   ├── architecture.md
│   ├── api-reference.md
│   └── deployment.md
│
├── requirements.txt         # Dependencias Python
├── .env.example            # Plantilla de variables de entorno
├── .gitignore
└── README.md
```

---

## 🤝 Contribuciones

Este proyecto está diseñado con arquitectura profesional inspirada en patrones **.NET 8** y **Domain-Driven Design (DDD)** para garantizar:

- ✨ **Escalabilidad Horizontal**: Arquitectura de microservicios independientes
- 🔒 **Seguridad de Nivel Empresarial**: JWT, roles granulares, auditoría completa
- 📊 **Mantenibilidad a Largo Plazo**: Código limpio, bien documentado y testeado
- 🚀 **Alto Rendimiento**: Streaming de respuestas, cache inteligente, operaciones asíncronas
- 🧪 **Testeable**: Cobertura de tests unitarios e integración

---

## 🐛 Troubleshooting

### Problemas Comunes

**Error: "No se puede conectar con Django"**
```bash
# Verificar que Django esté corriendo en el puerto 8001
curl http://localhost:8001/api/health

# Si no responde, revisar logs:
cd src/data-layer
python manage.py runserver 8001 --verbosity 2
```

**Error: "OpenAI API Key inválida"**
```bash
# Verificar que la variable de entorno esté configurada
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows

# Verificar en el archivo .env
cat .env | grep OPENAI_API_KEY
```

**Error: "JWT Token expirado"**
- Simplemente vuelve a iniciar sesión en el dashboard
- Los tokens tienen duración de 30 minutos por defecto

**Error: "Paciente no encontrado"**
- Verifica que el paciente esté registrado en Django Admin
- Comprueba que el ID del paciente sea correcto
- Revisa los logs de auditoría para más detalles

---

## 📞 Soporte

Para reportar problemas o sugerir mejoras:

1. 🐛 Usa el sistema de **issues** del repositorio
2. 📧 Contacta al equipo de desarrollo
3. 📖 Consulta la documentación técnica en `/docs`
4. 💬 Únete a nuestro canal de Slack/Discord

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

**Sistema de IA Médica Especializada en Producción** 🚀  

Transformando la gestión clínica mediante **Agentes Autónomos** e **Inteligencia Artificial**

`#AIHealthcare #LangGraph #FastAPI #Streamlit #Django #MedicalAI #BigData #AgenticAI`

---

*Desarrollado con ❤️ para revolucionar la atención médica mediante IA de vanguardia*

**Versión**: 2.0.0  
**Última actualización**: Enero 2025  
**Mantenido por**: Equipo OmniCare AI (Autor y Desarrollador: Jorge Herraiz Soler)