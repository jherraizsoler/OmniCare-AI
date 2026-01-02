from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import uvicorn
from langchain_core.messages import HumanMessage

# Importamos tu grafo y tu estado
from .graph_engine import medical_graph 
from .state import AgentState

app = FastAPI(title="OmniCare AI Engine")

# Modelos para la API (Pydantic)
class MedicalQuery(BaseModel):
    # Usamos Field para mapear lo que viene de .NET a variables de Python
    patient_id: str = Field(alias="patientId")
    symptoms: str
    urgency_level: int = Field(alias="urgencyLevel")
    consent_provided: bool = Field(alias="consentProvided")

    class Config:
        populate_by_name = True # Permite usar ambos nombres

class AiResponse(BaseModel):
    analysis: str
    recommended_actions: List[str]
    agent_in_charge: str

@app.post("/analyze", response_model=AiResponse)
async def analyze_medical_case(query: MedicalQuery):
    # 1. Preparamos el estado inicial para LangGraph según tu TypedDict en state.py
    initial_state = {
        "messages": [HumanMessage(content=f"El paciente presenta: {query.symptoms}")],
        "patient_data": {"patient_id": query.patient_id},
        "resource_focus": "Consulta General", # Valor inicial según tu state.py
        "safety_check_passed": False
    }

    # 2. Ejecutamos el grafo de forma asíncrona
    # Esto disparará: Retriever -> Analyst -> Ethics Reviewer
    final_state = await medical_graph.ainvoke(initial_state)

    # 3. Extraemos el contenido del último mensaje (el del Agente de Ética)
    final_answer = final_state["messages"][-1].content
    
    # Determinamos quién fue el último agente en tocar el mensaje
    # Si safety_check_passed es True, viene del revisor de ética
    agent_name = "Ethics_Reviewer_Agent" if final_state.get("safety_check_passed") else "Medical_Analyst_Agent"

    return AiResponse(
        analysis=final_answer,
        recommended_actions=["Seguir indicaciones del reporte", "Agendar cita de seguimiento"],
        agent_in_charge=agent_name
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)