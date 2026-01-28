# main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, AsyncGenerator
import uvicorn
import json
from pydantic import ConfigDict
from langchain_core.messages import HumanMessage

# Importamos tu grafo y tu estado
from ai_engine.graph_engine import medical_graph
from ai_engine.state import AgentState

app = FastAPI(title="OmniCare AI Engine")

# Modelos para la API (Pydantic)
class MedicalQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    patient_id: str = Field(alias="patientId")
    symptoms: str
    urgency_level: int = Field(alias="urgencyLevel")
    consent_provided: bool = Field(alias="consentProvided")


class AiResponse(BaseModel):
    analysis: str
    recommended_actions: List[str]
    agent_in_charge: str

@app.post("/analyze", response_model=AiResponse)
async def analyze_medical_case(query: MedicalQuery):
    """Endpoint estándar (Síncrono para el cliente)"""
    initial_state = {
        "messages": [HumanMessage(content=f"El paciente presenta: {query.symptoms}")],
        "patient_data": {"patient_id": query.patient_id},
        "resource_focus": "Consulta General",
        "safety_check_passed": False
    }

    final_state = await medical_graph.ainvoke(initial_state)
    final_answer = final_state["messages"][-1].content
    
    agent_name = "Ethics_Reviewer_Agent" if final_state.get("safety_check_passed") else "Medical_Analyst_Agent"

    return AiResponse(
        analysis=final_answer,
        recommended_actions=["Seguir indicaciones del reporte", "Agendar cita de seguimiento"],
        agent_in_charge=agent_name
    )

@app.post("/analyze-stream")
async def analyze_medical_case_stream(query: MedicalQuery):
    """Endpoint con Streaming (Tokens en tiempo real)"""
    
    initial_state = {
        "messages": [HumanMessage(content=f"El paciente presenta: {query.symptoms}")],
        "patient_data": {"patient_id": query.patient_id},
        "resource_focus": "Consulta General",
        "safety_check_passed": False
    }

    async def generate_events() -> AsyncGenerator[str, None]:
        # Usamos astream_events (v2) para capturar tokens del LLM mientras se generan
        async for event in medical_graph.astream_events(initial_state, version="v2"):
            kind = event["event"]
            
            # Detectamos cuando el modelo de chat genera un fragmento (chunk) de texto
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Formato Server-Sent Events (SSE)
                    yield f"data: {json.dumps({'token': content})}\n\n"
            
            # Opcional: Notificar cuando un agente específico termina
            elif kind == "on_chain_end" and event["name"] == "ethics_node":
                yield f"data: {json.dumps({'status': 'completed'})}\n\n"

    return StreamingResponse(generate_events(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)