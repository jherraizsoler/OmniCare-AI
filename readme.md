# 🏥 OmniCare AI: Sistema de Agentes Médicos Autónomos

Este proyecto demuestra una arquitectura de microservicios de alto impacto que combina un orquestador en **.NET 8**, un motor de inteligencia con **LangGraph** y una capa de datos persistente en **Django**.

---

## 🚀 Guía de Inicio Rápido

Para poner en marcha el sistema completo, abre **tres terminales** y sigue estos pasos:

---

### 1. Capa de Datos (Django - Puerto 8001)

Gestiona la persistencia de historiales clínicos y registros de auditoría.

```bash
# Navegar a la carpeta
cd src/data-layer

# Activar entorno virtual
source ../../venv/Scripts/activate

# Levantar el servicio
python manage.py runserver 8001
```
> **Importante:**  
> Accede a `http://localhost:8001/admin` y asegúrate de que el paciente **PAC-001** esté registrado.

---

## 2. Motor de IA (FastAPI + LangGraph - Puerto 8000)

El **“Cerebro”** que ejecuta el grafo de agentes autónomos  
(**Retriever → Analyst → Ethics**).

```bash
# Navegar a la carpeta
cd src

# Activar entorno virtual
source ../../venv/Scripts/activate

# Levantar FastAPI
uvicorn ai-engine.main:app --host 0.0.0.0 --port 8000 --reload
```

> **Nota:**  
> Verifica que el archivo `.env` contenga tu `OPENAI_API_KEY` para usar **GPT-4o-mini**.

---

## 3. Orquestador Backend (.NET 8 - Puerto 5129)

El punto de entrada principal que valida reglas de negocio y expone la API.

```bash
# Navegar a la carpeta
cd src/backend-core/OmniCare.Api

# Ejecutar con Hot Reload
dotnet watch run
```

## 🛠️ Cómo Probar el Sistema (Scalar)

Una vez que los tres servicios estén activos:

1. Abre tu navegador en:  
   `http://localhost:5129/scalar/v1`

2. Busca el endpoint:  
   `POST /api/ConsultaMedica/analizar`

3. Haz clic en **"Test Request"**

4. Usa el siguiente JSON de ejemplo:

```json
{
  "patientId": "PAC-001",
  "symptoms": "Dolor de cabeza agudo y antecedentes de hipertensión",
  "urgencyLevel": 2,
  "consentProvided": true
}
```

## 🧠 Arquitectura de Agentes (LangGraph)

El sistema utiliza un diseño de software sólido con los siguientes agentes:

- **Retriever Agent**: Conecta con Django para obtener el contexto clínico real.
- **Medical Analyst Agent**: Utiliza **GPT-4o-mini** para procesar síntomas e historial.
- **Ethics Reviewer Agent**: Valida la seguridad de la respuesta antes de enviarla al paciente.

---

¡Seguimos avanzando en la especialización de IA y Big Data! 🚀  
`#AI #SoftwareArchitecture #LangGraph #DotNet8`
