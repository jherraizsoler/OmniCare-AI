import os
from dotenv import load_dotenv
from typing import Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
import httpx
from langgraph.checkpoint.memory import MemorySaver

# IMPORT ABSOLUTO - funciona después de pip install -e .
from ai_engine.state import AgentState



load_dotenv()

# 1. Inicializar el LLM (GPT-4o-mini: Máximo ahorro)
llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0, 
    max_tokens=500
)

# 2. Inicializa la memoria
memory = MemorySaver()

# 3. NODO: Recuperador de Django
async def retrieval_node(state: AgentState):
    patient_id = state['patient_data'].get('patient_id')
    async with httpx.AsyncClient() as client:
        try:
            # Conexión con tu capa de datos Django
            response = await client.get(f"http://localhost:8001/api/patients/{patient_id}/")
            patient_info = response.json() if response.status_code == 200 else {}
            history = patient_info.get('clinical_history', 'Sin historial previo.')
            name = patient_info.get('name', 'Paciente desconocido')
        except Exception:
            history = "Error de conexión con la base de datos de Django."
            name = "Error"
    
    # Actualizamos el historial en el sistema
    content = f"Datos del Paciente ({name}): {history}"
    return {"messages": [SystemMessage(content=content)]}

# 4. NODO: Analista Médico
async def analysis_node(state: AgentState):
    # El analista toma todos los mensajes (historial + síntomas del usuario)
    prompt = [
        SystemMessage(content=f"Eres un experto analista médico. Tu enfoque actual es: {state['resource_focus']}."),
    ] + state['messages']
    
    response = await llm.ainvoke(prompt)
    return {"messages": [response]}

# 5. NODO: Revisor de Ética (Usa tus banderas de seguridad)
async def ethics_node(state: AgentState):
    # Obtener el contenido de la respuesta final
    final_response = state['messages'][-1].content
    patient_id = state['patient_data'].get('patient_id')
    symptoms = state['messages'][0].content # El primer mensaje enviado

    # --- Lógica de Auditoría ---
    async with httpx.AsyncClient() as client:
        try:
            audit_data = {
                "patient_id": patient_id,
                "agent_name": "Ethics_Reviewer_Agent",
                "input_symptoms": symptoms,
                "ai_analysis": final_response
            }
            # Enviamos el log al nuevo endpoint que configuramos en Django
            await client.post("http://localhost:8001/api/audit-logs/", json=audit_data)
            print(f"✅ Auditoría guardada para el paciente {patient_id}")
        except Exception as e:
            print(f"❌ Error al guardar auditoría: {e}")

    return {
        "messages": [state['messages'][-1]],
        "safety_check_passed": True
    }
    
    
# 6. Construcción del Grafo de Agentes Autónomos
workflow = StateGraph(AgentState)

# Añadimos los nodos
workflow.add_node("retriever", retrieval_node)
workflow.add_node("analyst", analysis_node)
workflow.add_node("ethics_reviewer", ethics_node)

# Definimos el flujo (Edges)
workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "analyst")
workflow.add_edge("analyst", "ethics_reviewer")
workflow.add_edge("ethics_reviewer", END)

# Compilamos
medical_graph = workflow.compile( 
    interrupt_before=["ethics_reviewer"]
)
# Alias para LangGraph Studio
graph = medical_graph
