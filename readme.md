# 🏥 OmniCare AI: Sistema de Agentes Médicos Autónomos

Sistema inteligente de análisis médico que combina un motor de IA basado en **LangGraph**, una capa de datos en **Django**, y una interfaz interactiva con **Streamlit**. Arquitectura de microservicios diseñada para consultas médicas asistidas por IA con auditoría completa.

---

## 🚀 Guía de Inicio Rápido

Para poner en marcha el sistema completo, abre **tres terminales** y sigue estos pasos en orden:

---

### 1. Capa de Datos (Django - Puerto 8001)

Gestiona la persistencia de historiales clínicos, autenticación de usuarios y registros de auditoría.
```bash
# Navegar a la carpeta del proyecto Django
cd ruta/a/tu/proyecto/django

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
> - Accede a `http://localhost:8001/admin` para gestionar usuarios y pacientes
> - Asegúrate de que el paciente **PAC-001** esté registrado para las pruebas
> - Este servicio debe estar corriendo antes de iniciar los demás componentes

---

## 2. Motor de IA (FastAPI + LangGraph - Puerto 8000)

El **"Cerebro"** que ejecuta el grafo de agentes autónomos  
(**Retriever → Analyst → Ethics Reviewer**).
```bash
# Navegar a la carpeta donde está main.py
cd ruta/donde/esta/main.py

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Levantar FastAPI
python main.py

# O alternativamente con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> **Requisitos:**  
> - Archivo `.env` con tu `OPENAI_API_KEY` para usar **GPT-4o-mini**
> - Instalar dependencias: `pip install fastapi uvicorn langchain-openai langgraph httpx python-dotenv`

**Endpoints disponibles:**
- `POST /analyze` - Análisis médico estándar (respuesta completa)
- `POST /analyze-stream` - Análisis con streaming (tokens en tiempo real)

---

## 3. Dashboard Interactivo (Streamlit)

Interfaz de usuario para médicos y pacientes con chat en tiempo real y visualización de métricas.
```bash
# Navegar a la carpeta donde está dashboard.py
cd ruta/donde/esta/dashboard.py

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Levantar Streamlit
streamlit run dashboard.py
```

> **Acceso:**  
> El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Funcionalidades:**
- 🔐 Sistema de login/registro
- 💬 Chat inteligente con streaming de respuestas
- 📊 Visualización de métricas en tiempo real (Dolor, Urgencia, Riesgo)
- 📋 Historial completo de consultas médicas
- 📈 Gráficos de evolución del paciente

---

## 🧪 Cómo Probar el Sistema

### Opción 1: A través del Dashboard (Recomendado)

1. Accede a `http://localhost:8501`
2. Crea una cuenta o inicia sesión
3. En la pestaña **"💬 Nueva Consulta"**, describe los síntomas
4. Observa el análisis en tiempo real con métricas actualizadas
5. Revisa el historial en **"📋 Portal del Paciente"**

### Opción 2: API REST con Scalar (Documentación Interactiva)

1. Asegúrate de que FastAPI esté corriendo en el puerto 8000
2. Abre tu navegador en: `http://localhost:8000/docs`
3. Explora la documentación interactiva de Swagger UI

**O utiliza Scalar para una mejor experiencia:**

1. Accede a: `http://localhost:8000/scalar/v1`
2. Busca el endpoint: `POST /analyze`
3. Haz clic en **"Try it out"** o **"Test Request"**
4. Usa el siguiente JSON de ejemplo:
```json
{
  "patientId": "PAC-001",
  "symptoms": "Dolor de cabeza agudo y antecedentes de hipertensión",
  "urgencyLevel": 2,
  "consentProvided": true
}
```

5. Haz clic en **"Execute"** para ver la respuesta del sistema

> **Nota:** Scalar ofrece una interfaz más moderna y fácil de usar que Swagger UI para probar tus endpoints.

### Opción 3: Streaming de tokens (cURL)
```bash
curl -X POST "http://localhost:8000/analyze-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": "PAC-001",
    "symptoms": "Fiebre alta y tos persistente",
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

### 2. **Medical Analyst Agent**
- Utiliza **GPT-4o-mini** (optimizado para costos)
- Analiza síntomas combinados con historial médico
- Genera diagnósticos preliminares y recomendaciones

### 3. **Ethics Reviewer Agent**
- Valida la seguridad de las respuestas generadas
- Registra cada interacción en la base de datos de auditoría
- Garantiza trazabilidad completa del sistema

**Flujo de ejecución:**
```
Consulta → Retriever → Analyst → Ethics Reviewer → Respuesta + Auditoría
```

---

## 📦 Stack Tecnológico

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Motor de IA** | LangGraph + LangChain | Orquestación de agentes |
| **LLM** | OpenAI GPT-4o-mini | Análisis médico |
| **API Backend** | FastAPI | Endpoints REST y streaming |
| **Base de Datos** | Django + SQLite/PostgreSQL | Persistencia y auditoría |
| **Frontend** | Streamlit | Dashboard interactivo |
| **Visualización** | Matplotlib | Gráficos y métricas |
| **Documentación** | Swagger UI + Scalar | API Explorer interactivo |

---

## 📋 Requisitos del Sistema
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

**Librerías principales:**
- `langgraph` - Orquestación de agentes
- `langchain-openai` - Integración con GPT
- `fastapi` y `uvicorn` - API REST
- `streamlit` - Dashboard web
- `django` - Backend y base de datos
- `httpx` - Cliente HTTP asíncrono
- `matplotlib` - Visualización de datos
- `python-dotenv` - Variables de entorno

---

## 🔒 Seguridad y Auditoría

- ✅ Autenticación JWT para todos los usuarios
- ✅ Registro completo de todas las consultas médicas
- ✅ Trazabilidad de respuestas generadas por IA
- ✅ Validación ética antes de entregar resultados
- ✅ Consentimiento explícito requerido para análisis

---

## 🎯 Próximos Pasos

- [ ] Dashboard de métricas para administradores
- [ ] Soporte multilenguaje

---

## 📝 Notas de Desarrollo

**Variables de Entorno Requeridas (.env):**
```env
OPENAI_API_KEY=tu-api-key-aqui
DJANGO_SECRET_KEY=tu-secret-key
```

**Puertos Utilizados:**
- `8001` - Django (Backend)
- `8000` - FastAPI (Motor IA)
- `8501` - Streamlit (Dashboard)

**URLs de Documentación:**
- Swagger UI: `http://localhost:8000/docs`
- Scalar: `http://localhost:8000/scalar/v1`
- ReDoc: `http://localhost:8000/redoc`

---

¡Sistema de IA médica en producción! 🚀  
`#AI #Healthcare #LangGraph #FastAPI #Streamlit #Django`