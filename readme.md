# 🏥 OmniCare AI: Sistema de Agentes Médicos Autónomos
<p align="center">
  <img src="banner_OmniCare_AI.png" alt="OmniCare AI Banner" width="100%">
</p>

> **Arquitectura Híbrida**: Núcleo empresarial en **.NET 8**, 
> orquestación de agentes con **LangGraph**, depuración visual en **LangGraph Studio** > y persistencia de datos en **Django**.

![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)
![.NET 8](https://img.shields.io/badge/.NET-8+-purple.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Django](https://img.shields.io/badge/Django-5.0+-darkgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-purple.svg)
![LangGraph Studio](https://img.shields.io/badge/LangGraph_Studio-Integrated-orange.svg)
![License](https://img.shields.io/badge/License-©jherraizsoler-blue.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)
![Tests](https://img.shields.io/github/actions/workflow/status/tu-usuario/omnicare-ai/main.yml?label=tests&style=flat-square)
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen.svg?style=flat-square)


Sistema inteligente de análisis médico que combina un motor de IA basado en **LangGraph** con soporte para **LangGraph Studio**, una capa de datos en **Django**, y una interfaz interactiva con **Streamlit**. Arquitectura de microservicios diseñada para la automatización de procesos clínicos complejos con auditoría completa y gestión profesional por roles.

> **TL;DR** > Plataforma médica basada en agentes autónomos con LangGraph y **LangGraph Studio**, orquestada por .NET 8,  
> con IA en streaming, auditoría clínica, seguridad JWT y dashboards por rol.

---

## 📖 Índice
1. [🚀 Guía de Inicio Rápido](#-guía-de-inicio-rápido)
2. [🧠 Motor de IA (LangGraph)](#-motor-de-inteligencia-artificial-langgraph)
3. [🐳 Dockerización](#-dockerización-despliegue-profesional)
4. [🧪 Pruebas Automatizadas](#-pruebas-automatizadas)
5. [🔒 Seguridad y Auditoría](#-seguridad-y-auditoría-especializada)


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

Para poner en marcha el sistema completo, abre **cuatro terminales** y sigue estos pasos en orden:

---

### 1. Capa de Datos (Django - Puerto 8001)

Gestiona la persistencia de historiales clínicos, autenticación JWT y registros de auditoría.
```bash
# Navegar a la carpeta del proyecto Django
cd src/data-layer

# Activar entorno virtual (Windows)
..\..\venv\Scripts\Activate.ps1

# O en Linux/Mac
source ../../venv/bin/activate

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
cd src/ai_engine

# Activar entorno virtual (Windows)
..\..\venv\Scripts\Activate.ps1

# O en Linux/Mac
source ../../venv/bin/activate

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
cd src/ai_engine

# Activar entorno virtual (Windows)
..\..\venv\Scripts\Activate.ps1

# O en Linux/Mac
source ../../venv/bin/activate

# Levantar Streamlit
streamlit run dashboard.py
```

> **Acceso:**  
> El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`


### 4. 🖥️ Scalar API Backend Core (.NET 8)

Servicio principal que expone la API y gestiona el streaming de respuestas de IA.

```bash
# Navegar a la carpeta del Backend Core
cd src/backend-core/OmniCare.Api

# Ejecutar la aplicación
dotnet run

Ir a esta url: http://localhost:5129/scalar/v1
```
> **Tip 💡**  
> En **Scalar**, puedes usar el botón **"Test Request"** (como se muestra en la captura) para observar cómo los **tokens de la IA llegan uno a uno**, 
> gracias al soporte de **streaming en tiempo real** configurado en el backend.


---

### Dockerización

## 🐳 Dockerización: Despliegue Profesional

**OmniCare AI** está completamente contenedorizado para asegurar un entorno de ejecución idéntico en desarrollo y producción.


### Uso con Docker
```bash
# 1. Construir la imagen (asegúrate de estar en la raíz)
docker build -t omnicare-ai .

# 2. Ejecutar el contenedor (mapeo de puertos FastAPI y Streamlit)
docker run -p 8000:8000 -p 8501:8501 --env-file .env omnicare-ai
```

---

### 4. Sección de CI/CD (Añadir)
Documenta la automatización que configuramos en GitHub:

## ⚙️ Integración Continua (CI/CD)

El repositorio utiliza **GitHub Actions** (`.github/workflows/main.yml`) para validar cada cambio automáticamente:

1. **Setup**: Configuración de entorno Python 3.11.
2. **Testing**: Ejecución automática de la suite de `pytest`.
3. **Build Check**: Validación de construcción de la imagen **Docker**.
4. **Security**: Verificación de secretos y variables de entorno.

## 🧪 Pruebas Automatizadas

El proyecto incluye una suite de pruebas para validar tanto la lógica individual de los agentes como la integración global del sistema **OmniCare AI**.


### Ejecución de Tests (PowerShell)

Para ejecutar los tests detectados en la estructura actual, utiliza los siguientes comandos desde la raíz del proyecto:

```powershell
# 1. Validación del Motor de IA (FastAPI + LangGraph)
# Verifica la lógica de los agentes, estados y nodos.
pytest src/ai_engine/tests/test_basic.py

# 2. Validación de Integración Global
# Asegura la comunicación entre el core y las capas de datos.
pytest tests/test_core.py
```

### ⚙️ Configuración de Testing

* **Framework**: `pytest` con soporte para `pytest-asyncio` (necesario para la naturaleza asíncrona de LangGraph).
* **Configuración**: El archivo `pytest.ini` en la raíz define los parámetros por defecto y los marcadores de asincronía.
* **Aislamiento**: Se recomienda ejecutar los tests con el entorno virtual activado para asegurar que todas las dependencias de `requirements.txt` estén disponibles y no haya conflictos de versiones.

---


### 👥 Funcionalidades por Rol

El sistema adapta su interfaz y lógica de negocio dinámicamente según el perfil del usuario autenticado:

#### 🟣 Vista Supervisor (Admin & Big Data)
* **📊 Dashboard de Métricas Globales**: Visualización de KPIs críticos y rendimiento del sistema en tiempo real.
* **👥 Gestión de Facultativos**: Control total sobre el alta, baja y administración del personal médico.
* **🔍 Auditoría de Agentes**: Supervisión detallada de los logs de la IA para garantizar la seguridad clínica.
* **📈 Análisis de Big Data**: Identificación de tendencias patológicas y estadísticas operativas a gran escala.
* **🛠️ Configuración de Sistema**: Gestión de parámetros de red y variables de entorno del core empresarial.

#### 🔵 Vista Médico (Clinical Operations)
* **🆕 Registro de Pacientes**: Capacidad exclusiva para dar de alta a nuevos pacientes en el sistema.
* **📌 Auto-asignación de Casos**: Gestión directa de la relación médico-paciente y asignación de expedientes.
* **💬 Diagnóstico Asistido**: Chat inteligente orquestado por **LangGraph** con respuesta en streaming.
* **📄 Exportación de Informes**: Generación y descarga de informes clínicos oficiales en formato PDF.
* **📊 Monitor de Evolución**: Herramientas visuales para el seguimiento de la mejoría y métricas del paciente.

#### 🟢 Vista Paciente (Personal Care)
* **🏥 Portal de Salud Personal**: Acceso seguro a su historial médico y recomendaciones recibidas.
* **💬 Triaje Inteligente**: Chat de asistencia inicial para la evaluación de urgencia de síntomas.
* **📈 Seguimiento de Constantes**: Gráficos interactivos de niveles de Dolor, Urgencia y Riesgo.
* **📅 Registro de Actividad**: Consulta cronológica de interacciones y visitas anteriores.

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

### Opción 4: 🛠️ Depuración y Orquestación con LangGraph Studio


Para garantizar la fiabilidad del triaje clínico, **OmniCare AI** es totalmente compatible con **LangGraph Studio**. Esta integración permite una observabilidad profunda y en tiempo real del flujo de decisiones de los agentes médicos.

### 🌟 Beneficios de la Integración
* **Visualización en Tiempo Real:** Interfaz gráfica para observar la transición de estados entre nodos (Diagnóstico Presuntivo -> Evaluación de Riesgo -> Recomendación).
* **Time-Travel Debugging:** Capacidad para retroceder a estados anteriores del triaje, modificar variables y re-ejecutar nodos para testear diversos escenarios médicos.
* **Hot Reloading:** Los cambios en la lógica de los agentes se reflejan instantáneamente sin reiniciar el servicio.

### ⚙️ Configuración del Entorno
Para que el Studio reconozca el flujo de agentes, asegúrate de tener el archivo `langgraph.json` en la raíz del proyecto con la siguiente estructura:

```json
{
  "dependencies": ["."],
  "graphs": {
    "medical_triage": "./omnicare/agents/graph.py:graph"
  },
  "env": ".env"
}
```


### 🚀 Ejecución y Acceso

Para levantar el servidor de desarrollo local y habilitar la visualización, utiliza **PowerShell** en la raíz del proyecto:

```powershell
# Configurar el path y arrancar el servidor de desarrollo
$env:PYTHONPATH="."; langgraph dev
```
Una vez el servidor esté activo, puedes interactuar con el grafo y monitorizar los hilos de ejecución directamente desde la **Web** a través de la interfaz de LangChain Smith:

🔗 **[🎨 Acceder a LangGraph Studio UI](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)**

> **Nota:** Esta interfaz web se conecta a tu servidor local en el puerto `2024`, permitiendo depurar el razonamiento de los agentes de **OmniCare AI** de forma visual sin instalaciones adicionales. Esto asegura la integridad y trazabilidad de los procesos para **OMNICARE_AI**.

---

## 🧠 Arquitectura de Agentes (LangGraph) con Integración .NET

El sistema utiliza un grafo de agentes autónomos coordinado mediante un pipeline híbrido donde **.NET 8** actúa como el orquestador de negocio y **Python** como el motor de razonamiento:

### 1. **Retriever Agent**
- Conecta con la capa de datos de Django y los servicios core de .NET para obtener el historial clínico.
- Recupera datos mediante API REST y servicios inyectados en el contenedor de dependencias de **ASP.NET Core**.
- Implementa patrones de resiliencia similares a *Polly* en .NET para manejar errores de conexión.

### 2. **Medical Analyst Agent**
- Utiliza **GPT-4o-mini** para procesar los datos estructurados provenientes del **Backend Core**.
- Analiza síntomas combinados con metadatos enriquecidos por la lógica de negocio en C#.
- Genera diagnósticos preliminares que son validados por las reglas de negocio de .NET antes de su entrega.

### 3. **Ethics Reviewer Agent**
- Valida la seguridad de las respuestas y asegura el cumplimiento normativo (GDPR/HIPAA).
- Registra cada interacción en los logs de auditoría compartidos.
- Utiliza filtros éticos avanzados para prevenir la generación de contenido sensible.

**Flujo de Ejecución Híbrido:**

Consulta del Usuario (Streamlit)  
↓  
Backend Core (.NET 8) → Validación de Reglas de Negocio  
↓  
LangGraph Engine (Python) → Orquestación de Agentes  
↓  
Retriever (Django) ↔ Analyst (GPT) ↔ Ethics Reviewer  
↓  
Respuesta en Streaming vía Scalar / WebSockets

---

**Características Avanzadas:**
- ✅ Manejo de estado robusto con `AgentState`
- ✅ Persistencia de contexto entre agentes
- ✅ Recuperación automática ante fallos
- ✅ Logging detallado para debugging
- ✅ Streaming de respuestas en tiempo real

---

---

## 📊 Arquitectura Técnica

| Componente | Tecnología | Rol / Patrón .NET Equivalente |
|------------|------------|-------------------------------|
| **Frontend** | Streamlit | Interfaz de Usuario Reactiva |
| **Backend Core** | **.NET 8 (C#)** | **Enterprise Business Logic / Web API** |
| **Orquestador** | LangGraph | Workflow Engine / AI Agent Orchestrator |
| **Observabilidad** | **LangSmith** | Tracing, Debugging y Evaluación de LLM |
| **Contenedores** | **Docker** | **Aislamiento y Despliegue Consistente** |
| **CI/CD** | **GitHub Actions** | **Pipeline de Integración y Entrega Continua** |
| **Data Layer** | Django 5.0 | Persistence Layer / Entity Framework Pattern |
| **Seguridad** | **JWT / .env** | **Bearer Token Auth & Secret Management** |

## 🧪 Calidad de Software y Testing

Para garantizar la fiabilidad del triaje médico y la integridad de los datos de **Abbant**, el sistema cuenta con una suite de pruebas automatizadas.



### Ejecución de Pruebas
```powershell
# Ejecutar tests de integración y motor de IA
pytest src/ai_engine/tests/test_basic.py
```
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
# --- Framework Core (Django para Persistencia & API) ---
django>=5.1.0
djangorestframework>=3.15.0
djangorestframework-simplejwt>=5.4.0
django-cors-headers>=4.4.0
psycopg2-binary>=2.9.9

# --- Servidor & Validación (Compatibilidad FastAPI/Uvicorn) ---
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.10.0
pydantic-settings>=2.7.0
scalar-fastapi

# --- Inteligencia Artificial (Ecosistema LangChain 0.3/0.4) ---
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.4.1
langchain-openai>=0.2.0
langgraph>=0.2.0
langgraph-checkpoint>=2.1.0
langgraph-cli
langsmith>=0.2.0

# --- Dashboard & Visualización ---
streamlit>=1.52.0
matplotlib>=3.10.0
numpy>=1.26.0
pandas>=2.2.0

# --- Comunicación & Utilidades ---
httpx>=0.28.0
python-dotenv>=1.0.0
typing-extensions>=4.12.0

# --- Generación de Reportes Clínicos ---
reportlab>=4.2.0

# --- Testing & CI/CD ---
pytest>=8.0.0
pytest-mock>=3.12.0
pytest-asyncio>=0.23.0
```

---
## 🔧 Configuración del Entorno (.env)

Para el correcto funcionamiento de **OmniCare AI**, asegúrate de configurar las siguientes variables en tu archivo `.env` local:

```env
# OpenAI Configuration
OPENAI_API_KEY=tu_api_key_aqui

# LangSmith Tracking (Observabilidad y Debugging del Motor de IA)
LANGSMITH_TRACKING=true
LANGSMITH_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGSMITH_API_KEY=tu_langsmith_key_aqui
LANGSMITH_PROJECT="OmniCare-AI-Dev"

# Django Configuration
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Opcional, por defecto usa SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/omnicare

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Puertos y Host de Servicios
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
STREAMLIT_SERVER_PORT=8501
```
> [!CAUTION]
> **Recordatorio de Seguridad**: Este archivo `.env` contiene credenciales sensibles. Nunca lo compartas ni lo subas a GitHub. Debe estar listado en tu `.gitignore`.

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

### 📂 Estructura del Proyecto
```text
OmniCare-AI/
├── src/
│   ├── ai_engine/               # Motor de IA (FastAPI + LangGraph)
│   │   ├── main.py              # API Gateway del motor de IA
│   │   ├── graph_engine.py      # Lógica de orquestación de estados (LangGraph)
│   │   ├── state.py             # Definición de esquemas y estados de agentes
│   │   ├── dashboard.py         # Interfaz de usuario (Streamlit)
│   │   └── tests/               # Pruebas unitarias del motor de IA
│   │
│   ├── backend-core/            # Núcleo Empresarial (.NET 8)
│   │   ├── OmniCare.Api/        # Endpoints de negocio y servicios C#
│   │   │   ├── Controllers/     # Controladores (Consulta Médica, etc.)
│   │   │   ├── Services/        # Lógica de Asistente Médico
│   │   │   └── Program.cs       # Configuración y Dependency Injection
│   │   └── OmniCare.sln         # Solución global de Visual Studio
│   │
│   └── data-layer/              # Capa de Persistencia (Django 5.0)
│       ├── medical_records/     # Gestión de pacientes, consultas y auditoría
│       │   ├── models.py        # Modelos ORM (Patient, AI Audit Log)
│       │   ├── views.py         # Lógica de la API REST de datos
│       │   └── serializers.py   # Transformación de datos para la API
│       ├── omnicare_db/         # Configuración del servidor Django
│       └── manage.py            # CLI de administración de Django
│
├── tests/                       # Suite de pruebas de integración global
├── media/                       # Activos visuales y capturas del sistema
├── .langgraph_api/              # Checkpoints y almacenamiento local de LangGraph
├── deployments/                 # Archivos de configuración de despliegue
├── Dockerfile                   # Configuración de contenerización
├── requirements.txt             # Dependencias de Python
├── pyproject.toml               # Configuración del proyecto y herramientas
└── README.md                    # Documentación principal
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

Este proyecto esta bajo derechos de autor Jorge Herraiz Soler no se puede utilizar para fines comerciales ni lucrativos.

---

**Sistema de IA Médica Especializada en Producción** 🚀  

Transformando la gestión clínica mediante **Agentes Autónomos** e **Inteligencia Artificial**

`#AIHealthcare #LangGraph #FastAPI #Streamlit #Django #MedicalAI #BigData #AgenticAI`

---

*Desarrollado con ❤️ para revolucionar la atención médica mediante IA de vanguardia*

**Versión**: 2.0.0  
**Última actualización**: Enero 2025  
**Mantenido por**: Equipo OmniCare AI (Autor y Desarrollador: Jorge Herraiz Soler)
